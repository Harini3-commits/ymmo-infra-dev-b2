from typing import Optional
from pydantic import BaseModel


# ---------- Property ----------

class PropertyBase(BaseModel):
    title: str
    city: str
    price: float

    status: Optional[str] = "a_vendre"

    image_url: Optional[str] = None
    address: Optional[str] = None

    # Détails
    surface: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    type: Optional[str] = None
    description: Optional[str] = None

    # Coordonnées
    lat: Optional[float] = None
    lng: Optional[float] = None


class PropertyCreate(PropertyBase):
    pass


class PropertyRead(PropertyBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Client ----------

class ClientBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    type: Optional[str] = "acheteur"


class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Transaction ----------

class TransactionBase(BaseModel):
    property_id: int
    client_id: int
    price: float
    date: str          # ex: "2026-06-10"

    # type d'opération : vente ou location
    operation_type: str  # "vente" ou "location"

    status: Optional[str] = "terminee"


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: int

    class Config:
        from_attributes = True