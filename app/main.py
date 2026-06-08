from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import properties, clients

app = FastAPI()

# Créer les tables dans la BDD (si elles n'existent pas)
Base.metadata.create_all(bind=engine)

# Inclure les routes
app.include_router(properties.router)
app.include_router(clients.router)


@app.get("/ping")
def ping():
    return {"message": "pong"}