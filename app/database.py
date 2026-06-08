from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Fichier SQLite local
SQLALCHEMY_DATABASE_URL = "sqlite:///./ymmo.db"

# Pour SQLite, il faut ce paramètre
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()