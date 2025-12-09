import cv2
import numpy as np
import mediapipe as mp
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import io
import pickle
from typing import List, Tuple, Optional, Dict
from pathlib import Path
import os

from app.core.config import get_settings
from app.models.face import Face
from sqlalchemy.orm import Session

settings = get_settings()


class FaceRecognitionService:
    """Service for face detection and recognition using MediaPipe and OpenCV"""
    
    def __init__(self):
        # Initialize MediaPipe Face Detection and Face Mesh
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_face_mesh = mp.solutions.face_mesh
        
        # Face Detection model
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,  # 0 for short-range, 1 for full-range
            min_detection_confidence=0.5
        )
        
        # Face Mesh for feature extraction
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            min_detection_confidence=0.5
        )
        
        self.tolerance = settings.FACE_RECOGNITION_TOLERANCE
    
    def detect_faces(self, image_path: str) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in an image using MediaPipe
        
        Args:
            image_path: Path to image file
            
        Returns:
            List of face locations (top, right, bottom, left)
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            results = self.face_detection.process(image_rgb)
            
            face_locations = []
            if results.detections:
                h, w, _ = image.shape
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    
                    # Convert relative coordinates to absolute
                    left = int(bbox.xmin * w)
                    top = int(bbox.ymin * h)
                    right = int((bbox.xmin + bbox.width) * w)
                    bottom = int((bbox.ymin + bbox.height) * h)
                    
                    # Return in format (top, right, bottom, left)
                    face_locations.append((top, right, bottom, left))
            
            return face_locations
        except Exception as e:
            raise Exception(f"Error detecting faces: {str(e)}")
    
    def get_face_encoding(self, image_path: str) -> Optional[np.ndarray]:
        """
        Get face encoding from image using MediaPipe Face Mesh
        
        Args:
            image_path: Path to image file
            
        Returns:
            Face encoding array or None if no face detected
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process with Face Mesh
            results = self.face_mesh.process(image_rgb)
            
            if not results.multi_face_landmarks:
                return None
            
            # Extract landmarks from first face
            face_landmarks = results.multi_face_landmarks[0]
            
            # Create feature vector from landmarks (468 landmarks with x, y, z)
            encoding = []
            for landmark in face_landmarks.landmark:
                encoding.extend([landmark.x, landmark.y, landmark.z])
            
            return np.array(encoding, dtype=np.float32)
        
        except Exception as e:
            raise Exception(f"Error getting face encoding: {str(e)}")
    
    def compare_faces(
        self, 
        known_encoding: np.ndarray, 
        unknown_encoding: np.ndarray
    ) -> Tuple[bool, float]:
        """
        Compare two face encodings using cosine similarity
        
        Args:
            known_encoding: Known face encoding
            unknown_encoding: Unknown face encoding
            
        Returns:
            Tuple of (is_match, distance)
        """
        try:
            # Calculate cosine similarity
            similarity = cosine_similarity(
                known_encoding.reshape(1, -1),
                unknown_encoding.reshape(1, -1)
            )[0][0]
            
            # Convert similarity to distance (0 = identical, 1 = different)
            distance = 1 - similarity
            
            # Check if match (lower distance = better match)
            is_match = distance <= self.tolerance
            
            return is_match, float(distance)
        except Exception as e:
            raise Exception(f"Error comparing faces: {str(e)}")
    
    def search_face(
        self, 
        query_encoding: np.ndarray, 
        db: Session,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Search for similar faces in database
        
        Args:
            query_encoding: Face encoding to search for
            db: Database session
            top_k: Number of top results to return
            
        Returns:
            List of matching faces with confidence scores
        """
        try:
            # Get all faces from database
            all_faces = db.query(Face).all()
            
            if not all_faces:
                return []
            
            results = []
            
            for face in all_faces:
                # Deserialize encoding
                known_encoding = pickle.loads(face.encoding)
                
                # Compare faces
                is_match, distance = self.compare_faces(known_encoding, query_encoding)
                
                # Calculate confidence (inverse of distance)
                confidence = max(0, (1 - distance) * 100)
                
                results.append({
                    "face": face.to_dict(),
                    "distance": float(distance),  # Convert numpy to Python float
                    "confidence": round(float(confidence), 2),  # Convert to Python float
                    "is_match": bool(is_match)  # Convert numpy.bool_ to Python bool
                })
            
            # Sort by distance (lower is better)
            results.sort(key=lambda x: x["distance"])
            
            # Return top_k results
            return results[:top_k]
        except Exception as e:
            raise Exception(f"Error searching face: {str(e)}")
    
    def encode_face_to_bytes(self, encoding: np.ndarray) -> bytes:
        """Serialize face encoding to bytes"""
        return pickle.dumps(encoding)
    
    def decode_face_from_bytes(self, encoding_bytes: bytes) -> np.ndarray:
        """Deserialize face encoding from bytes"""
        return pickle.loads(encoding_bytes)
    
    def save_uploaded_file(self, file_content: bytes, filename: str) -> str:
        """
        Save uploaded file to disk
        
        Args:
            file_content: File content in bytes
            filename: Original filename
            
        Returns:
            Path to saved file
        """
        try:
            # Create upload directory if not exists
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            
            # Generate unique filename
            import uuid
            file_ext = Path(filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
            
            # Save file
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            return file_path
        except Exception as e:
            raise Exception(f"Error saving file: {str(e)}")
    
    def validate_image(self, file_content: bytes) -> bool:
        """
        Validate if file is a valid image
        
        Args:
            file_content: File content in bytes
            
        Returns:
            True if valid image, False otherwise
        """
        try:
            Image.open(io.BytesIO(file_content))
            return True
        except:
            return False
    
    def draw_face_boxes(
        self, 
        image_path: str, 
        face_locations: List[Tuple[int, int, int, int]],
        output_path: str = None
    ) -> str:
        """
        Draw boxes around detected faces
        
        Args:
            image_path: Path to input image
            face_locations: List of face locations
            output_path: Path to save output image (optional)
            
        Returns:
            Path to output image
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            
            # Draw rectangles around faces
            for (top, right, bottom, left) in face_locations:
                # Draw rectangle
                cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
                
                # Add label
                cv2.putText(
                    image, 
                    "Face", 
                    (left, top - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, 
                    (0, 255, 0), 
                    2
                )
            
            # Generate output path if not provided
            if not output_path:
                input_path = Path(image_path)
                output_path = str(input_path.parent / f"{input_path.stem}_detected{input_path.suffix}")
            
            # Save image
            cv2.imwrite(output_path, image)
            
            return output_path
        except Exception as e:
            raise Exception(f"Error drawing face boxes: {str(e)}")
    
    def __del__(self):
        """Cleanup MediaPipe resources"""
        if hasattr(self, 'face_detection'):
            self.face_detection.close()
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()


# Create singleton instance
face_recognition_service = FaceRecognitionService()
