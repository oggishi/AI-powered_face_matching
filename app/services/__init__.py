"""Services package initialization"""
from app.services.face_recognition_service import get_face_service

# Create global instance
face_recognition_service = get_face_service()

__all__ = ["face_recognition_service"]
