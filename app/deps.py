"""Session de base de données partagée (dépendance FastAPI)."""

from collections.abc import Generator

from sqlalchemy.orm import Session

from .database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Fournit une session ORM et la ferme proprement après usage."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
