from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("/", response_model=schemas.ClientRead)
def create_client(client_in: schemas.ClientCreate, db: Session = Depends(get_db)):
    # Vérifier si email déjà utilisé
    existing = db.query(models.Client).filter(models.Client.email == client_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_client = models.Client(
        first_name=client_in.first_name,
        last_name=client_in.last_name,
        email=client_in.email,
        phone=client_in.phone,
        type=client_in.type,
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@router.get("/", response_model=List[schemas.ClientRead])
def list_clients(db: Session = Depends(get_db)):
    clients = db.query(models.Client).all()
    return clients


@router.get("/{client_id}", response_model=schemas.ClientRead)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return {"detail": "Client deleted"}