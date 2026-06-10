from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/")
def get_stats(db: Session = Depends(get_db)):
    total_properties = db.query(models.Property).count()
    sold_properties = db.query(models.Property).filter(models.Property.status == "vendu").count()
    total_clients = db.query(models.Client).count()
    total_transactions = db.query(models.Transaction).count()

    # Total du chiffre d'affaires (somme du prix des transactions)
    total_revenue = 0.0
    for tr in db.query(models.Transaction).all():
        total_revenue += tr.price

    return {
        "total_properties": total_properties,
        "sold_properties": sold_properties,
        "total_clients": total_clients,
        "total_transactions": total_transactions,
        "total_revenue": total_revenue,
    }