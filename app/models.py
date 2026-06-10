from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    city = Column(String, index=True)
    price = Column(Float)
    status = Column(String, default="a_vendre")  # a_vendre / vendu / a_louer / loue
    image_url = Column(String, nullable=True)    # URL d'image du bien
    address = Column(String, nullable=True)      # nouvelle colonne : adresse complète

    # Relation avec Transaction (un bien peut avoir plusieurs transactions)
    transactions = relationship("Transaction", back_populates="property")


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    type = Column(String, default="acheteur")  # acheteur / vendeur

    # Relation avec Transaction (un client peut avoir plusieurs transactions)
    transactions = relationship("Transaction", back_populates="client")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    price = Column(Float, nullable=False)
    date = Column(String, nullable=False)  # string rapide, ex "2026-06-10"
    status = Column(String, default="terminee")  # terminee, en_cours, etc.

    # Relations vers Property et Client
    property = relationship("Property", back_populates="transactions")
    client = relationship("Client", back_populates="transactions")