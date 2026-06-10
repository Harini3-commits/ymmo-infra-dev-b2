from typing import Optional
from pydantic import BaseModel


# ---------- Property ----------

class PropertyBase(BaseModel):
    title: str
    city: str
    price: float
    status: Optional[str] = "a_vendre"
    image_url: Optional[str] = None


class PropertyCreate(PropertyBase):
    pass


class PropertyRead(PropertyBase):
    id: int

    class Config:
        from_attributes = True  # lit les objets SQLAlchemy


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
    date: str          # ex: "2026-06-09"
    status: Optional[str] = "terminee"


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: int

    class Config:
        from_attributes = True