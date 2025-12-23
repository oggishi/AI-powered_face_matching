"""
Flower Recognition Service using Keras Transfer Learning

- Loads a trained Keras image classification model
- Predicts top-k flower classes with confidence scores
- Maps predictions to rich flower info in the database when available

Author: AI Assistant
Date: 2025-12-23
"""

from app.core.config import get_settings
import os
import io
import uuid
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image
from sqlalchemy.orm import Session

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image

# Preprocessing helper (EfficientNet default)
try:
    from tensorflow.keras.applications.efficientnet import preprocess_input as efficientnet_preprocess
except Exception:
    efficientnet_preprocess = None

logger = logging.getLogger(__name__)

settings = get_settings()


class FlowerRecognitionService:
    """Singleton service for flower image recognition"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FlowerRecognitionService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.model_path = settings.FLOWER_MODEL_PATH
        self.class_map_path = settings.FLOWER_CLASS_MAP_PATH
        self.top_k = settings.FLOWER_TOP_K

        self.model = None
        self.class_names: List[str] = []
        self.input_size: Tuple[int, int] = (224, 224)  # default

        # Load model if present
        try:
            if os.path.exists(self.model_path):
                logger.info(f"Loading flower model from {self.model_path}...")
                self.model = load_model(self.model_path)
                # Try to read input size from model config
                try:
                    input_shape = self.model.input_shape
                    if isinstance(input_shape, list):
                        input_shape = input_shape[0]
                    if input_shape and len(input_shape) >= 3:
                        self.input_size = (
                            int(input_shape[1]), int(input_shape[2]))
                except Exception:
                    pass
                logger.info("Flower model loaded successfully")
            else:
                logger.warning(
                    "Flower model not found. Please train and export the model.")
        except Exception as e:
            logger.error(f"Failed to load flower model: {e}")

        # Load class map
        try:
            if os.path.exists(self.class_map_path):
                with open(self.class_map_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Supports either dict {index: name} or list of names
                if isinstance(data, dict):
                    # Sort by index keys
                    self.class_names = [name for _, name in sorted(
                        ((int(k), v) for k, v in data.items()), key=lambda x: x[0])]
                elif isinstance(data, list):
                    self.class_names = data
                logger.info(
                    f"Loaded {len(self.class_names)} flower class names")
            else:
                logger.warning(
                    "Class map not found. Predictions will return numeric indices.")
        except Exception as e:
            logger.error(f"Failed to load class map: {e}")

        self._initialized = True

    # -------- Utilities --------
    def validate_image(self, file_content: bytes) -> bool:
        try:
            Image.open(io.BytesIO(file_content))
            return True
        except Exception:
            return False

    def save_uploaded_file(self, file_content: bytes, filename: str) -> str:
        try:
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            file_ext = Path(filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
            with open(file_path, "wb") as f:
                f.write(file_content)
            return file_path
        except Exception as e:
            raise Exception(f"Error saving file: {str(e)}")

    # -------- Prediction --------
    def _preprocess_image(self, image_path: str) -> np.ndarray:
        """Load and preprocess image for model inference"""
        img = keras_image.load_img(image_path, target_size=self.input_size)
        x = keras_image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        # If EfficientNet preprocess is available, use it
        if efficientnet_preprocess:
            x = efficientnet_preprocess(x)
        else:
            # Simple normalization
            x = x / 255.0
        return x

    def predict(self, image_path: str, top_k: Optional[int] = None) -> Dict[str, Any]:
        """Predict flower class for an image"""
        if self.model is None:
            return {
                "success": False,
                "message": "Flower model not loaded. Train the model first.",
                "predictions": []
            }
        try:
            x = self._preprocess_image(image_path)
            preds = self.model.predict(x)
            preds = np.array(preds)
            if preds.ndim == 1:
                preds = np.expand_dims(preds, axis=0)
            probs = preds[0]

            k = top_k or self.top_k
            top_indices = probs.argsort()[-k:][::-1]
            predictions = []
            for idx in top_indices:
                class_name = self.class_names[idx] if idx < len(
                    self.class_names) else str(idx)
                predictions.append({
                    "class_index": int(idx),
                    "class_name": class_name,
                    "confidence": float(probs[idx])
                })

            return {
                "success": True,
                "predictions": predictions,
                "message": f"Predicted top-{k} classes"
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {
                "success": False,
                "message": str(e),
                "predictions": []
            }

    # -------- DB Integration --------
    def find_flower_info(self, db: Session, class_name: str) -> Optional[Dict[str, Any]]:
        """Find flower info by class_name in DB (common or Vietnamese name)"""
        try:
            from app.models.flower import Flower
            q = db.query(Flower).filter(
                (Flower.common_name.ilike(class_name)) |
                (Flower.vietnamese_name.ilike(class_name))
            ).first()
            return q.to_dict() if q else None
        except Exception as e:
            logger.warning(f"Lookup flower info failed: {e}")
            return None

    def save_recognition_result(
        self,
        db: Session,
        query_image_path: str,
        predicted_class_name: str,
        confidence: float,
        top_predictions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        try:
            from app.models.flower import Flower, FlowerRecognitionResult
            # Try to resolve predicted flower
            predicted_flower = db.query(Flower).filter(
                Flower.common_name.ilike(predicted_class_name)).first()
            res = FlowerRecognitionResult(
                query_image_path=query_image_path,
                predicted_flower_id=predicted_flower.id if predicted_flower else None,
                predicted_class_name=predicted_class_name,
                confidence=confidence,
                top_predictions=top_predictions,
                model_version="keras-transfer-v1"
            )
            db.add(res)
            db.commit()
            db.refresh(res)
            return res.to_dict()
        except Exception as e:
            logger.warning(f"Failed to save recognition result: {e}")
            return {}

    # -------- External Knowledge (optional) --------
    def fetch_wikipedia_summary(self, name: str, lang: str = 'vi') -> Optional[Dict[str, Any]]:
        """Fetch brief info from Wikipedia REST API for a flower name.
        Tries Vietnamese first, then English.
        """
        import requests

        def fetch(lang_code: str):
            try:
                url = f"https://{lang_code}.wikipedia.org/api/rest_v1/page/summary/{name}"
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    return {
                        "title": data.get("title"),
                        "extract": data.get("extract"),
                        "description": data.get("description"),
                        "lang": lang_code,
                        "content_urls": data.get("content_urls", {}),
                        "thumbnail": data.get("thumbnail", {})
                    }
            except Exception as e:
                logger.debug(f"Wikipedia fetch error ({lang_code}): {e}")
            return None
        info = fetch(lang)
        if not info:
            info = fetch('en')
        return info


def get_flower_service() -> FlowerRecognitionService:
    return FlowerRecognitionService()
