from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.config import get_settings
from app.models.flower import Flower
from app.services import flower_recognition_service

settings = get_settings()
router = APIRouter(prefix="/api/flowers", tags=["flower-recognition"])


@router.post("/recognize")
async def recognize_flower(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Recognize flower from uploaded image and return rich info"""
    try:
        # Validate file type
        if not file.filename.lower().endswith(tuple(settings.allowed_extensions_list)):
            raise HTTPException(
                status_code=400, detail=f"Invalid file type. Allowed: {', '.join(settings.allowed_extensions_list)}")

        content = await file.read()
        if not flower_recognition_service.validate_image(content):
            raise HTTPException(status_code=400, detail="Invalid image file")
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")

        # Save file
        file_path = flower_recognition_service.save_uploaded_file(
            content, file.filename)

        # Predict
        pred_result = flower_recognition_service.predict(
            file_path, top_k=settings.FLOWER_TOP_K)
        if not pred_result.get("success"):
            raise HTTPException(status_code=500, detail=pred_result.get(
                "message", "Prediction failed"))

        top_predictions = pred_result["predictions"]
        best = top_predictions[0] if top_predictions else None

        # Lookup DB info
        flower_info = None
        if best:
            flower_info = flower_recognition_service.find_flower_info(
                db, best["class_name"]) or None
            # If no DB info, attempt Wikipedia summary as fallback
            if not flower_info:
                wiki = flower_recognition_service.fetch_wikipedia_summary(
                    best["class_name"]) or None
            else:
                wiki = None

        # Save recognition history
        saved = {}
        if best:
            saved = flower_recognition_service.save_recognition_result(
                db=db,
                query_image_path=file_path,
                predicted_class_name=best["class_name"],
                confidence=best["confidence"],
                top_predictions=top_predictions
            )

        return {
            "success": True,
            "query_image": file_path,
            "top_predictions": top_predictions,
            "best_prediction": best,
            "flower_info": flower_info,
            "external_info": wiki,
            "history_id": saved.get("id") if saved else None
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
async def list_flowers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List flower records in database"""
    try:
        flowers = db.query(Flower).offset(skip).limit(limit).all()
        return {
            "success": True,
            "count": len(flowers),
            "flowers": [f.to_dict() for f in flowers]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def add_flower(
    common_name: str = Form(...),
    scientific_name: Optional[str] = Form(None),
    vietnamese_name: Optional[str] = Form(None),
    family: Optional[str] = Form(None),
    genus: Optional[str] = Form(None),
    species: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    origin: Optional[str] = Form(None),
    characteristics: Optional[str] = Form(None),
    habitat: Optional[str] = Form(None),
    meaning: Optional[str] = Form(None),
    symbolism: Optional[str] = Form(None),
    cultural_significance: Optional[str] = Form(None),
    care_instructions: Optional[str] = Form(None),
    blooming_season: Optional[str] = Form(None),
    colors: Optional[str] = Form(None),  # JSON string list
    uses: Optional[str] = Form(None),
    medicinal_properties: Optional[str] = Form(None),
    image_path: Optional[str] = Form(None),
    additional_info: Optional[str] = Form(None),  # JSON string
    db: Session = Depends(get_db)
):
    """Add or update a flower information record"""
    import json
    try:
        flower = Flower(
            common_name=common_name,
            scientific_name=scientific_name,
            vietnamese_name=vietnamese_name,
            family=family,
            genus=genus,
            species=species,
            description=description,
            origin=origin,
            characteristics=characteristics,
            habitat=habitat,
            meaning=meaning,
            symbolism=symbolism,
            cultural_significance=cultural_significance,
            care_instructions=care_instructions,
            blooming_season=blooming_season,
            colors=json.loads(colors) if colors else None,
            uses=uses,
            medicinal_properties=medicinal_properties,
            image_path=image_path,
            additional_info=json.loads(
                additional_info) if additional_info else None,
        )
        db.add(flower)
        db.commit()
        db.refresh(flower)
        return {"success": True, "flower": flower.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
