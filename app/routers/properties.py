from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/properties", tags=["properties"])


@router.post("/", response_model=schemas.PropertyRead)
def create_property(property_in: schemas.PropertyCreate, db: Session = Depends(get_db)):
    if property_in.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than 0")

    db_property = models.Property(
        title=property_in.title,
        city=property_in.city,
        price=property_in.price,
        status=property_in.status,
        image_url=property_in.image_url,
        address=property_in.address,
        surface=property_in.surface,
        bedrooms=property_in.bedrooms,
        bathrooms=property_in.bathrooms,
        type=property_in.type,
        description=property_in.description,
        lat=property_in.lat,
        lng=property_in.lng,
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


@router.put("/{property_id}", response_model=schemas.PropertyRead)
def update_property(property_id: int, property_in: schemas.PropertyCreate, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    if property_in.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than 0")

    prop.title = property_in.title
    prop.city = property_in.city
    prop.price = property_in.price
    prop.status = property_in.status
    prop.image_url = property_in.image_url
    prop.address = property_in.address
    prop.surface = property_in.surface
    prop.bedrooms = property_in.bedrooms
    prop.bathrooms = property_in.bathrooms
    prop.type = property_in.type
    prop.description = property_in.description
    prop.lat = property_in.lat
    prop.lng = property_in.lng

    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop


@router.delete("/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    db.delete(prop)
    db.commit()
    return {"detail": "Property deleted"}