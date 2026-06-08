from typing import Optional
from pydantic import BaseModel


# ---------- Property ----------

class PropertyBase(BaseModel):
    title: str
    city: str
    price: float
    status: Optional[str] = "a_vendre"


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