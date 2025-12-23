"""
Flower Database Models
Lưu trữ thông tin chi tiết về các loài hoa

Author: AI Assistant
Date: 2025-12-22
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON
from sqlalchemy.sql import func
from app.core.database import Base
import json


class Flower(Base):
    """Flower model - Thông tin chi tiết về các loài hoa"""
    __tablename__ = "flowers"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Thông tin cơ bản
    common_name = Column(String, nullable=False, index=True)  # Tên thông thường (ví dụ: "Hoa hồng")
    scientific_name = Column(String, nullable=True, index=True)  # Tên khoa học (ví dụ: "Rosa")
    vietnamese_name = Column(String, nullable=True)  # Tên tiếng Việt
    
    # Phân loại
    family = Column(String, nullable=True)  # Họ (ví dụ: "Rosaceae")
    genus = Column(String, nullable=True)  # Chi (ví dụ: "Rosa")
    species = Column(String, nullable=True)  # Loài
    
    # Thông tin chi tiết
    description = Column(Text, nullable=True)  # Mô tả chi tiết
    origin = Column(Text, nullable=True)  # Xuất xứ, lịch sử
    characteristics = Column(Text, nullable=True)  # Đặc điểm nhận dạng
    habitat = Column(Text, nullable=True)  # Môi trường sống
    
    # Ý nghĩa và văn hóa
    meaning = Column(Text, nullable=True)  # Ý nghĩa, biểu tượng
    symbolism = Column(Text, nullable=True)  # Tượng trưng cho điều gì
    cultural_significance = Column(Text, nullable=True)  # Ý nghĩa văn hóa
    
    # Thông tin trồng trọt
    care_instructions = Column(Text, nullable=True)  # Hướng dẫn chăm sóc
    blooming_season = Column(String, nullable=True)  # Mùa nở hoa
    colors = Column(JSON, nullable=True)  # Màu sắc có thể có (list)
    
    # Sử dụng và lợi ích
    uses = Column(Text, nullable=True)  # Công dụng (trang trí, dược liệu, etc.)
    medicinal_properties = Column(Text, nullable=True)  # Tính chất dược liệu
    
    # Hình ảnh mẫu
    image_path = Column(String, nullable=True)  # Đường dẫn ảnh đại diện
    
    # Thông tin bổ sung (JSON flexible)
    additional_info = Column(JSON, nullable=True)  # Thông tin bổ sung khác
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "common_name": self.common_name,
            "scientific_name": self.scientific_name,
            "vietnamese_name": self.vietnamese_name,
            "family": self.family,
            "genus": self.genus,
            "species": self.species,
            "description": self.description,
            "origin": self.origin,
            "characteristics": self.characteristics,
            "habitat": self.habitat,
            "meaning": self.meaning,
            "symbolism": self.symbolism,
            "cultural_significance": self.cultural_significance,
            "care_instructions": self.care_instructions,
            "blooming_season": self.blooming_season,
            "colors": self.colors,
            "uses": self.uses,
            "medicinal_properties": self.medicinal_properties,
            "image_path": self.image_path,
            "additional_info": self.additional_info,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class FlowerRecognitionResult(Base):
    """Flower Recognition Result - Lưu lịch sử nhận diện"""
    __tablename__ = "flower_recognition_results"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Thông tin ảnh query
    query_image_path = Column(String, nullable=False)
    
    # Kết quả nhận diện
    predicted_flower_id = Column(Integer, nullable=True)  # ID của flower trong DB
    predicted_class_name = Column(String, nullable=True)  # Tên class từ model
    confidence = Column(Float, nullable=True)  # Độ tin cậy (0-1)
    
    # Top-k predictions (JSON)
    top_predictions = Column(JSON, nullable=True)  # List of {class_name, confidence}
    
    # Metadata
    model_version = Column(String, nullable=True)  # Phiên bản model
    processing_time = Column(Float, nullable=True)  # Thời gian xử lý (seconds)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "query_image_path": self.query_image_path,
            "predicted_flower_id": self.predicted_flower_id,
            "predicted_class_name": self.predicted_class_name,
            "confidence": self.confidence,
            "top_predictions": self.top_predictions,
            "model_version": self.model_version,
            "processing_time": self.processing_time,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class FlowerImage(Base):
    """Flower Image - Lưu trữ ảnh training và reference"""
    __tablename__ = "flower_images"
    
    id = Column(Integer, primary_key=True, index=True)
    flower_id = Column(Integer, nullable=False, index=True)  # Link to Flower
    image_path = Column(String, nullable=False)
    image_type = Column(String, nullable=True)  # "training", "reference", "user_upload"
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "flower_id": self.flower_id,
            "image_path": self.image_path,
            "image_type": self.image_type,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
