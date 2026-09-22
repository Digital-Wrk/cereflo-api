"""Point d'entrée de l'API Cereflo — le flux de la pensée."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import Base, engine
from .routers import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crée les tables au démarrage (en attendant Alembic)."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Cereflo API",
    description="API REST de gestion de tâches — *cerebrum* + *flow*.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(tasks.router)


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    """Message d'accueil de l'API."""
    return {"message": "Bienvenue sur Cereflo API 🧠", "docs": "/docs"}


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Sonde de disponibilité (pour les healthchecks)."""
    return {"status": "ok"}
