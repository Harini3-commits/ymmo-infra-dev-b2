from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    city = Column(String, index=True)
    price = Column(Float)
    status = Column(String, default="a_vendre")  # a_vendre / vendu


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    type = Column(String, default="acheteur")  # acheteur / vendeur