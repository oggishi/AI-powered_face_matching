from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, Float
from sqlalchemy.sql import func
from app.core.database import Base
import json


class Face(Base):
    """Face model for database"""
    __tablename__ = "faces"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    image_path = Column(String, nullable=False)
    encoding = Column(LargeBinary, nullable=False)  # Store face encoding as binary
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image_path": self.image_path,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class MatchResult(Base):
    """Match result model for storing search history"""
    __tablename__ = "match_results"
    
    id = Column(Integer, primary_key=True, index=True)
    query_image_path = Column(String, nullable=False)
    matched_face_id = Column(Integer, nullable=True)
    distance = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "query_image_path": self.query_image_path,
            "matched_face_id": self.matched_face_id,
            "distance": self.distance,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
