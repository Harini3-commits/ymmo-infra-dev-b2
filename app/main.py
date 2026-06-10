from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models
from app.routers import properties, clients, transactions, stats

app = FastAPI()

# Autoriser les requêtes depuis ton front (fichier ouvert en local)
origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "null",  # important pour les fichiers ouverts en file://
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # autorise GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)

# Créer les tables dans la BDD (si elles n'existent pas)
Base.metadata.create_all(bind=engine)

# Inclure les routes
app.include_router(properties.router)
app.include_router(clients.router)
app.include_router(transactions.router)
app.include_router(stats.router)


@app.get("/ping")
def ping():
    return {"message": "pong"}