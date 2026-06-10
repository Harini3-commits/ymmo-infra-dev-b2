from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=schemas.TransactionRead)
def create_transaction(
    transaction_in: schemas.TransactionCreate,
    db: Session = Depends(get_db),
):
    # Vérifier que le bien existe
    prop = db.query(models.Property).filter(models.Property.id == transaction_in.property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    # Vérifier que le client existe
    client = db.query(models.Client).filter(models.Client.id == transaction_in.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Créer la transaction
    db_tr = models.Transaction(
        property_id=transaction_in.property_id,
        client_id=transaction_in.client_id,
        price=transaction_in.price,
        date=transaction_in.date,
        status=transaction_in.status,
    )
    db.add(db_tr)

    # Mettre à jour le statut du bien en "vendu" si la transaction est terminée
    if transaction_in.status == "terminee":
        prop.status = "vendu"
        db.add(prop)

    db.commit()
    db.refresh(db_tr)
    return db_tr


@router.get("/", response_model=List[schemas.TransactionRead])
def list_transactions(db: Session = Depends(get_db)):
    trs = db.query(models.Transaction).all()
    return trs


@router.get("/{transaction_id}", response_model=schemas.TransactionRead)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    tr = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not tr:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tr


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    tr = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not tr:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(tr)
    db.commit()
    return {"detail": "Transaction deleted"}