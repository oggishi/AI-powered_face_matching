from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from pathlib import Path

from app.core.database import get_db
from app.core.config import get_settings
from app.models.face import Face, MatchResult
from app.services import face_recognition_service

settings = get_settings()
router = APIRouter(prefix="/api", tags=["face-recognition"])


@router.post("/detect-face")
async def detect_face(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Detect faces in uploaded image
    
    Returns:
        - Number of faces detected
        - Face locations
        - Image path with drawn boxes
        - Warning if multiple faces detected
        - Cropped face images
    """
    try:
        # Validate file
        if not file.filename.lower().endswith(tuple(settings.ALLOWED_EXTENSIONS)):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Read file content
        content = await file.read()
        
        # Validate image
        if not face_recognition_service.validate_image(content):
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Check file size
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        # Save file
        file_path = face_recognition_service.save_uploaded_file(content, file.filename)
        
        # Detect faces
        face_locations = face_recognition_service.detect_faces(file_path)
        
        # Draw boxes around faces
        output_path = None
        cropped_faces = []
        warning = None
        
        if face_locations:
            output_path = face_recognition_service.draw_face_boxes(file_path, face_locations)
            
            # ⚠️ Warning if multiple faces
            if len(face_locations) > 1:
                warning = f"⚠️ Multiple faces detected ({len(face_locations)}). For Add to Database, please use single-face images."
            
            # 🔪 Auto-crop each face
            cropped_faces = face_recognition_service.crop_faces(file_path, face_locations)
        
        return {
            "success": True,
            "num_faces": len(face_locations),
            "face_locations": face_locations,
            "original_image": file_path,
            "detected_image": output_path,
            "cropped_faces": cropped_faces,
            "warning": warning,
            "message": f"Detected {len(face_locations)} face(s)" if face_locations else "No faces detected"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-face")
async def add_face(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Add a new face to the database
    
    Args:
        file: Image file containing face
        name: Name of the person
        description: Optional description
    
    Returns:
        Created face record
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(tuple(settings.ALLOWED_EXTENSIONS)):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Read and validate file
        content = await file.read()
        if not face_recognition_service.validate_image(content):
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        # Save file
        file_path = face_recognition_service.save_uploaded_file(content, file.filename)
        
        # Get face encoding
        encoding = face_recognition_service.get_face_encoding(file_path)
        
        if encoding is None:
            # Clean up file
            os.remove(file_path)
            raise HTTPException(
                status_code=400,
                detail="No face detected in image. Please upload a clear face image."
            )
        
        # Serialize encoding
        encoding_bytes = face_recognition_service.encode_face_to_bytes(encoding)
        
        # Create database record
        new_face = Face(
            name=name,
            description=description,
            image_path=file_path,
            encoding=encoding_bytes
        )
        
        db.add(new_face)
        db.commit()
        db.refresh(new_face)
        
        return {
            "success": True,
            "face": new_face.to_dict(),
            "message": f"Successfully added face for {name}"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch-add-faces")
async def batch_add_faces(
    file: UploadFile = File(...),
    names: str = Form(...),  # Comma-separated names
    db: Session = Depends(get_db)
):
    """
    🔥 Batch add multiple faces from one image with multiple people
    
    Args:
        file: Image file containing multiple faces
        names: Comma-separated names (e.g., "John, Jane, Bob")
    
    Returns:
        List of added faces
    """
    try:
        # Validate file
        if not file.filename.lower().endswith(tuple(settings.ALLOWED_EXTENSIONS)):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Read and validate
        content = await file.read()
        if not face_recognition_service.validate_image(content):
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Save file
        file_path = face_recognition_service.save_uploaded_file(content, file.filename)
        
        # Detect faces
        face_locations = face_recognition_service.detect_faces(file_path)
        
        if not face_locations:
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="No faces detected")
        
        # Parse names
        name_list = [n.strip() for n in names.split(',')]
        
        if len(name_list) != len(face_locations):
            os.remove(file_path)
            raise HTTPException(
                status_code=400,
                detail=f"Mismatch: {len(face_locations)} faces detected but {len(name_list)} names provided"
            )
        
        # Crop faces
        cropped_faces = face_recognition_service.crop_faces(file_path, face_locations)
        
        # Add each face to database
        added_faces = []
        for idx, (cropped_path, name) in enumerate(zip(cropped_faces, name_list)):
            # Get encoding
            encoding = face_recognition_service.get_face_encoding(cropped_path)
            
            if encoding is not None:
                encoding_bytes = face_recognition_service.encode_face_to_bytes(encoding)
                
                new_face = Face(
                    name=name,
                    description=f"Auto-added from batch (face #{idx + 1})",
                    image_path=cropped_path,
                    encoding=encoding_bytes
                )
                
                db.add(new_face)
                added_faces.append(name)
        
        db.commit()
        
        return {
            "success": True,
            "num_added": len(added_faces),
            "faces": added_faces,
            "message": f"Successfully added {len(added_faces)} face(s)"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search-face")
async def search_face(
    file: UploadFile = File(...),
    top_k: int = Form(5),
    db: Session = Depends(get_db)
):
    """
    Search for similar faces in database
    
    Args:
        file: Image file containing face to search
        top_k: Number of top results to return
    
    Returns:
        List of matching faces with confidence scores
    """
    try:
        # Validate file
        if not file.filename.lower().endswith(tuple(settings.ALLOWED_EXTENSIONS)):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Read and validate file
        content = await file.read()
        if not face_recognition_service.validate_image(content):
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Save file temporarily
        file_path = face_recognition_service.save_uploaded_file(content, file.filename)
        
        # Get face encoding
        encoding = face_recognition_service.get_face_encoding(file_path)
        
        if encoding is None:
            os.remove(file_path)
            raise HTTPException(
                status_code=400,
                detail="No face detected in image. Please upload a clear face image."
            )
        
        # Search for similar faces
        results = face_recognition_service.search_face(encoding, db, top_k)
        
        # Save match result for best match
        if results:
            best_match = results[0]
            match_result = MatchResult(
                query_image_path=file_path,
                matched_face_id=best_match["face"]["id"] if best_match["is_match"] else None,
                distance=best_match["distance"],
                confidence=best_match["confidence"]
            )
            db.add(match_result)
            db.commit()
        
        return {
            "success": True,
            "query_image": file_path,
            "num_results": len(results),
            "results": results,
            "message": f"Found {len(results)} matching face(s)" if results else "No matches found"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/faces")
async def get_all_faces(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all faces from database
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of face records
    """
    try:
        faces = db.query(Face).offset(skip).limit(limit).all()
        return {
            "success": True,
            "count": len(faces),
            "faces": [face.to_dict() for face in faces]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/faces/{face_id}")
async def get_face(
    face_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific face by ID"""
    try:
        face = db.query(Face).filter(Face.id == face_id).first()
        
        if not face:
            raise HTTPException(status_code=404, detail="Face not found")
        
        return {
            "success": True,
            "face": face.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/faces/{face_id}")
async def delete_face(
    face_id: int,
    db: Session = Depends(get_db)
):
    """Delete a face from database"""
    try:
        face = db.query(Face).filter(Face.id == face_id).first()
        
        if not face:
            raise HTTPException(status_code=404, detail="Face not found")
        
        # Delete image file
        if os.path.exists(face.image_path):
            os.remove(face.image_path)
        
        # Delete from database
        db.delete(face)
        db.commit()
        
        return {
            "success": True,
            "message": f"Successfully deleted face with ID {face_id}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/match-history")
async def get_match_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get match history"""
    try:
        results = db.query(MatchResult).order_by(
            MatchResult.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return {
            "success": True,
            "count": len(results),
            "results": [result.to_dict() for result in results]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get system statistics"""
    try:
        total_faces = db.query(Face).count()
        total_searches = db.query(MatchResult).count()
        
        return {
            "success": True,
            "stats": {
                "total_faces": total_faces,
                "total_searches": total_searches
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
