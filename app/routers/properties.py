from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/properties", tags=["properties"])


@router.post("/", response_model=schemas.PropertyRead)
def create_property(property_in: schemas.PropertyCreate, db: Session = Depends(get_db)):
    db_property = models.Property(
        title=property_in.title,
        city=property_in.city,
        price=property_in.price,
        status=property_in.status,
    )
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


@router.get("/", response_model=List[schemas.PropertyRead])
def list_properties(db: Session = Depends(get_db)):
    properties = db.query(models.Property).all()
    return properties


@router.get("/{property_id}", response_model=schemas.PropertyRead)
def get_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop


@router.delete("/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    db.delete(prop)
    db.commit()
    return {"detail": "Property deleted"}