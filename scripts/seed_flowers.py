"""
Seed initial flower records into the local database.

Run:
python scripts/seed_flowers.py
"""
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, init_db
from app.models.flower import Flower

SEED_DATA = [
    {
        "common_name": "Rose",
        "scientific_name": "Rosa",
        "vietnamese_name": "Hoa hồng",
        "family": "Rosaceae",
        "genus": "Rosa",
        "description": "Roses are a group of herbaceous shrubs found in temperate regions throughout both hemispheres.",
        "origin": "Cultivated since ancient times in the Mediterranean, Persia, and China.",
        "meaning": "Love, beauty, passion",
        "blooming_season": "Spring to fall",
        "colors": ["red", "pink", "white", "yellow", "orange"],
        "uses": "Ornamental, perfume, culinary"
    },
    {
        "common_name": "Sunflower",
        "scientific_name": "Helianthus annuus",
        "vietnamese_name": "Hoa hướng dương",
        "family": "Asteraceae",
        "genus": "Helianthus",
        "description": "Sunflowers are known for their large, daisy-like flower faces and bright yellow petals.",
        "origin": "Native to North America; cultivated by indigenous peoples.",
        "meaning": "Adoration, loyalty, longevity",
        "blooming_season": "Summer",
        "colors": ["yellow", "orange", "red"],
        "uses": "Ornamental, oil, edible seeds"
    },
    {
        "common_name": "Tulip",
        "scientific_name": "Tulipa",
        "vietnamese_name": "Hoa tulip",
        "family": "Liliaceae",
        "genus": "Tulipa",
        "description": "Tulips are spring-blooming perennials that grow from bulbs.",
        "origin": "Native to Central Asia; popularized in the Ottoman Empire and Netherlands.",
        "meaning": "Perfect love, elegance",
        "blooming_season": "Spring",
        "colors": ["red", "yellow", "pink", "purple", "white"],
        "uses": "Ornamental"
    },
    {
        "common_name": "Daisy",
        "scientific_name": "Bellis perennis",
        "vietnamese_name": "Hoa cúc",
        "family": "Asteraceae",
        "genus": "Bellis",
        "description": "Common daisy with white petals around a yellow center.",
        "origin": "Europe and western Asia.",
        "meaning": "Innocence, purity, new beginnings",
        "blooming_season": "Spring to fall",
        "colors": ["white", "pink"],
        "uses": "Ornamental"
    },
    {
        "common_name": "Dandelion",
        "scientific_name": "Taraxacum officinale",
        "vietnamese_name": "Bồ công anh",
        "family": "Asteraceae",
        "genus": "Taraxacum",
        "description": "Bright yellow flowers that turn into spherical seed heads.",
        "origin": "Europe and Asia; now worldwide.",
        "meaning": "Healing, hope, resilience",
        "blooming_season": "Spring",
        "colors": ["yellow"],
        "uses": "Herbal medicine, edible leaves and roots"
    },
]


def main():
    init_db()
    db: Session = SessionLocal()
    try:
        for item in SEED_DATA:
            exists = db.query(Flower).filter(
                Flower.common_name == item["common_name"]).first()
            if not exists:
                db.add(Flower(**item))
        db.commit()
        print("Seeded flower records.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
