"""Schémas Pydantic pour la validation et la sérialisation des tâches."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    """Champs communs à la création et à la lecture d'une tâche."""

    title: str = Field(..., min_length=1, max_length=200, examples=["Apprendre FastAPI"])
    description: str | None = Field(None, max_length=5000)
    done: bool = False


class TaskCreate(TaskBase):
    """Payload de création d'une tâche."""
    pass


class TaskUpdate(BaseModel):
    """Payload de mise à jour partielle (tous les champs optionnels)."""

    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=5000)
    done: bool | None = None


class TaskRead(TaskBase):
    """Représentation complète d'une tâche renvoyée par l'API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
