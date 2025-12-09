"""
ArcFace Face Recognition Service using DeepFace

Professional-grade face recognition:
- Models: VGG-Face, Facenet, Facenet512, OpenFace, DeepFace, DeepID, ArcFace, Dlib, SFace
- Default: ArcFace (99.82% accuracy on LFW)
- Embedding: 512-D for ArcFace
- Distance metrics: Cosine similarity

Author: AI Assistant
Date: 2025
"""

from deepface import DeepFace
import cv2
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import logging
from PIL import Image
import io
import os
import uuid
import pickle
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

# Import settings
from app.core.config import get_settings
settings = get_settings()


class FaceRecognitionService:
    """Professional face recognition using DeepFace (ArcFace model)"""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super(FaceRecognitionService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize DeepFace with ArcFace model"""
        if self._initialized:
            return
            
        print("🚀 Initializing DeepFace (ArcFace model)...")
        
        # Model configuration
        self.model_name = "ArcFace"  # Best accuracy: 99.82%
        self.distance_metric = "cosine"
        self.detector_backend = "retinaface"  # State-of-the-art detector (best)
        
        # Thresholds for ArcFace with cosine distance
        self.recognition_threshold = 0.68
        
        # Pre-load model (first call will download if needed)
        try:
            DeepFace.build_model(self.model_name)
            print(f"✅ {self.model_name} model loaded successfully!")
            print(f"   - Detector: {self.detector_backend}")
            print(f"   - Distance metric: {self.distance_metric}")
            print(f"   - Threshold: {self.recognition_threshold}")
        except Exception as e:
            logger.warning(f"Model pre-load warning: {e}")
        
        self._initialized = True
    
    def detect_face(self, image_path: str) -> Dict[str, Any]:
        """
        Detect face in image
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dict with detection result
        """
        try:
            # DeepFace extract_faces returns list of detected faces
            faces = DeepFace.extract_faces(
                img_path=str(image_path),
                detector_backend=self.detector_backend,
                enforce_detection=False
            )
            
            if not faces or len(faces) == 0:
                return {
                    "success": True,
                    "face_detected": False,
                    "bbox": None,
                    "confidence": 0.0,
                    "message": "No face detected"
                }
            
            # Get first/largest face
            face = faces[0]
            
            return {
                "success": True,
                "face_detected": True,
                "bbox": face.get("facial_area", None),
                "confidence": face.get("confidence", 0.0),
                "message": f"{len(faces)} face(s) detected"
            }
            
        except Exception as e:
            logger.error(f"Detection error: {str(e)}")
            return {
                "success": False,
                "face_detected": False,
                "bbox": None,
                "confidence": 0.0,
                "message": f"Error: {str(e)}"
            }
    
    def encode_face(self, image_path: str) -> Dict[str, Any]:
        """
        Generate face embedding using ArcFace
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dict with encoding result
        """
        try:
            # DeepFace.represent returns embeddings
            embeddings = DeepFace.represent(
                img_path=str(image_path),
                model_name=self.model_name,
                detector_backend=self.detector_backend,
                enforce_detection=True
            )
            
            if not embeddings:
                return {
                    "success": False,
                    "encoding": None,
                    "message": "No face detected for encoding"
                }
            
            # Get first face embedding
            embedding = np.array(embeddings[0]["embedding"])
            
            return {
                "success": True,
                "encoding": embedding,
                "bbox": embeddings[0].get("facial_area", None),
                "message": "Encoding generated successfully"
            }
            
        except ValueError as e:
            # No face detected
            return {
                "success": False,
                "encoding": None,
                "message": "No face detected in image"
            }
        except Exception as e:
            logger.error(f"Encoding error: {str(e)}")
            return {
                "success": False,
                "encoding": None,
                "message": f"Error: {str(e)}"
            }
    
    def compare_faces(
        self, 
        encoding1: np.ndarray, 
        encoding2: np.ndarray
    ) -> Dict[str, Any]:
        """
        Compare two face encodings using cosine similarity
        
        Args:
            encoding1: First face encoding
            encoding2: Second face encoding
            
        Returns:
            Dict with comparison result
        """
        try:
            # Compute cosine distance
            from scipy.spatial.distance import cosine
            distance = float(cosine(encoding1, encoding2))
            
            # Similarity (1 - distance)
            similarity = 1 - distance
            
            # Determine match
            is_match = distance <= self.recognition_threshold
            
            # Confidence percentage
            confidence = float(similarity * 100)
            
            return {
                "is_match": bool(is_match),
                "similarity": similarity,
                "distance": distance,
                "confidence": confidence
            }
            
        except Exception as e:
            logger.error(f"Comparison error: {str(e)}")
            return {
                "is_match": False,
                "similarity": 0.0,
                "distance": 2.0,
                "confidence": 0.0
            }
    
    def verify_face_match(
        self,
        image1_path: str,
        image2_path: str
    ) -> Dict[str, Any]:
        """
        Verify if two images contain the same person
        
        Args:
            image1_path: Path to first image
            image2_path: Path to second image
            
        Returns:
            Dict with verification result
        """
        try:
            # DeepFace.verify compares two images directly
            result = DeepFace.verify(
                img1_path=str(image1_path),
                img2_path=str(image2_path),
                model_name=self.model_name,
                detector_backend=self.detector_backend,
                distance_metric=self.distance_metric,
                enforce_detection=True
            )
            
            return {
                "success": True,
                "is_match": bool(result["verified"]),
                "distance": float(result["distance"]),
                "threshold": float(result["threshold"]),
                "similarity": float(1 - result["distance"]) if result["distance"] <= 1 else 0.0,
                "confidence": float((1 - result["distance"]) * 100) if result["distance"] <= 1 else 0.0,
                "message": "Verification completed"
            }
            
        except Exception as e:
            logger.error(f"Verification error: {str(e)}")
            return {
                "success": False,
                "is_match": False,
                "distance": 2.0,
                "message": f"Error: {str(e)}"
            }
    
    def crop_faces(self, image_path: str, face_locations: List[Tuple[int, int, int, int]]) -> List[str]:
        """
        🔥 Crop individual faces from an image with multiple people
        
        Args:
            image_path: Path to source image
            face_locations: List of face bounding boxes [(top, right, bottom, left), ...]
        
        Returns:
            List of paths to cropped face images
        """
        try:
            # Load image with CV2
            image = cv2.imread(str(image_path))
            
            if image is None:
                logger.error(f"Failed to load image: {image_path}")
                return []
            
            cropped_paths = []
            
            # Crop each face
            for idx, (top, right, bottom, left) in enumerate(face_locations):
                # Extract face region
                face_img = image[top:bottom, left:right]
                
                # Generate unique filename
                crop_filename = f"{uuid.uuid4()}_face_{idx}.jpg"
                crop_path = os.path.join(settings.UPLOAD_DIR, crop_filename)
                
                # Save cropped face
                cv2.imwrite(crop_path, face_img)
                cropped_paths.append(crop_path)
                
                logger.info(f"Cropped face {idx + 1}/{len(face_locations)} → {crop_filename}")
            
            return cropped_paths
            
        except Exception as e:
            logger.error(f"Crop faces error: {str(e)}")
            return []
    
    def process_image(self, image_path: str) -> Dict[str, Any]:
        """
        Complete pipeline: detect and encode face
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dict with encoding result
        """
        return self.encode_face(image_path)
    
    def search_similar_faces(
        self,
        query_encoding: np.ndarray,
        database_encodings: List[Tuple[Any, np.ndarray]],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar faces in database
        
        Args:
            query_encoding: Query face encoding
            database_encodings: List of (person_id, encoding) tuples
            top_k: Number of top results
            
        Returns:
            List of matches sorted by similarity
        """
        try:
            if not database_encodings:
                return []
            
            results = []
            for person_id, db_encoding in database_encodings:
                comparison = self.compare_faces(query_encoding, db_encoding)
                
                results.append({
                    "person_id": person_id,
                    "similarity": comparison["similarity"],
                    "distance": comparison["distance"],
                    "confidence": comparison["confidence"],
                    "is_match": comparison["is_match"]
                })
            
            # Sort by similarity (descending)
            results.sort(key=lambda x: x["similarity"], reverse=True)
            
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []
    
    def batch_encode_faces(
        self,
        image_paths: List[str],
        progress_callback: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """
        Batch process multiple images
        
        Args:
            image_paths: List of image paths
            progress_callback: Optional callback(index, total)
            
        Returns:
            List of encoding results
        """
        results = []
        total = len(image_paths)
        
        for idx, image_path in enumerate(image_paths):
            result = self.process_image(image_path)
            result["image_path"] = image_path
            results.append(result)
            
            if progress_callback:
                progress_callback(idx + 1, total)
        
        return results
    
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
            file_ext = Path(filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
            
            # Save file
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            return file_path
        except Exception as e:
            raise Exception(f"Error saving file: {str(e)}")
    
    def detect_faces(self, image_path: str) -> List[Tuple[int, int, int, int]]:
        """
        Detect ALL faces in an image (compatibility wrapper)
        
        Args:
            image_path: Path to image file
            
        Returns:
            List of face bounding boxes (top, right, bottom, left)
        """
        try:
            # DeepFace extract_faces returns ALL detected faces
            faces = DeepFace.extract_faces(
                img_path=str(image_path),
                detector_backend=self.detector_backend,
                enforce_detection=False
            )
            
            if not faces or len(faces) == 0:
                return []
            
            face_locations = []
            
            # Convert ALL faces from DeepFace format to MediaPipe format
            for face in faces:
                bbox = face.get("facial_area", None)
                if bbox:
                    # DeepFace bbox format: {'x': left, 'y': top, 'w': width, 'h': height}
                    top = bbox['y']
                    left = bbox['x']
                    bottom = bbox['y'] + bbox['h']
                    right = bbox['x'] + bbox['w']
                    
                    face_locations.append((top, right, bottom, left))
            
            return face_locations
        except Exception as e:
            logger.error(f"Face detection error: {str(e)}")
            return []
    
    def get_face_encoding(self, image_path: str) -> Optional[np.ndarray]:
        """
        Get face encoding from image (compatibility wrapper)
        
        Args:
            image_path: Path to image file
            
        Returns:
            Face encoding array (512-D) or None if no face detected
        """
        try:
            result = self.encode_face(image_path)
            
            if not result["success"] or result["encoding"] is None:
                return None
            
            return result["encoding"]
        except Exception as e:
            logger.error(f"Face encoding error: {str(e)}")
            return None
    
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
            face_locations: List of face locations (top, right, bottom, left)
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
    
    def encode_face_to_bytes(self, encoding: np.ndarray) -> bytes:
        """Serialize face encoding to bytes"""
        return pickle.dumps(encoding)
    
    def decode_face_from_bytes(self, encoding_bytes: bytes) -> np.ndarray:
        """Deserialize face encoding from bytes"""
        return pickle.loads(encoding_bytes)
    
    def search_face(
        self, 
        query_encoding: np.ndarray, 
        db: Session,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Search for similar faces in database
        
        Args:
            query_encoding: Face encoding to search for (512-D)
            db: Database session
            top_k: Number of top results to return
            
        Returns:
            List of matching faces with confidence scores
        """
        try:
            from app.models.face import Face
            
            # Get all faces from database
            all_faces = db.query(Face).all()
            
            if not all_faces:
                return []
            
            results = []
            
            for face in all_faces:
                # Deserialize encoding
                known_encoding = pickle.loads(face.encoding)
                
                # Compare faces using compare_faces method
                comparison = self.compare_faces(known_encoding, query_encoding)
                
                results.append({
                    "face": face.to_dict(),
                    "distance": comparison["distance"],
                    "confidence": comparison["confidence"],
                    "is_match": comparison["is_match"]
                })
            
            # Sort by similarity (higher is better)
            results.sort(key=lambda x: x["confidence"], reverse=True)
            
            # Return top_k results
            return results[:top_k]
        except Exception as e:
            raise Exception(f"Error searching face: {str(e)}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "model_name": self.model_name,
            "detector": self.detector_backend,
            "distance_metric": self.distance_metric,
            "embedding_size": 512,
            "accuracy": "99.82% (LFW benchmark)",
            "threshold": self.recognition_threshold,
            "status": "initialized" if self._initialized else "not initialized"
        }


def get_face_service() -> FaceRecognitionService:
    """Get singleton instance"""
    return FaceRecognitionService()
