"""Services package initialization"""
from app.services.face_recognition_service import get_face_service
from app.services.flower_recognition_service import get_flower_service

# Create global instances
face_recognition_service = get_face_service()
flower_recognition_service = get_flower_service()

__all__ = ["face_recognition_service", "flower_recognition_service"]
