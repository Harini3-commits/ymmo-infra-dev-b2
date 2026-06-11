from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=schemas.TransactionRead)
def create_transaction(transaction_in: schemas.TransactionCreate, db: Session = Depends(get_db)):
    # Vérifier que le bien existe
    prop = db.query(models.Property).filter(models.Property.id == transaction_in.property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    # Vérifier que le client existe
    client = db.query(models.Client).filter(models.Client.id == transaction_in.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    if transaction_in.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than 0")

    if transaction_in.operation_type not in ("vente", "location"):
        raise HTTPException(status_code=400, detail="operation_type must be 'vente' or 'location'")

    # Créer la transaction
    db_tx = models.Transaction(
        property_id=transaction_in.property_id,
        client_id=transaction_in.client_id,
        price=transaction_in.price,
        date=transaction_in.date,
        operation_type=transaction_in.operation_type,
        status=transaction_in.status,
    )
    db.add(db_tx)

    # LOGIQUE MÉTIER : mise à jour du statut du bien
    if transaction_in.operation_type == "vente":
        prop.status = "vendu"
    elif transaction_in.operation_type == "location":
        prop.status = "loue"

    db.add(prop)
    db.commit()
    db.refresh(db_tx)
    return db_tx


@router.get("/", response_model=List[schemas.TransactionRead])
def list_transactions(db: Session = Depends(get_db)):
    txs = db.query(models.Transaction).all()
    return txs


@router.get("/{transaction_id}", response_model=schemas.TransactionRead)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    tx = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    tx = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(tx)
    db.commit()
    return {"detail": "Transaction deleted"}