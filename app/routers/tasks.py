"""Endpoints CRUD pour les tâches."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[schemas.TaskRead])
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    done: bool | None = None,
    db: Session = Depends(get_db),
) -> list[models.Task]:
    """Lister les tâches (avec pagination et filtre optionnel sur `done`)."""
    stmt = select(models.Task).offset(skip).limit(min(limit, 100))
    if done is not None:
        stmt = stmt.where(models.Task.done == done)
    return list(db.scalars(stmt))


@router.post("", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)) -> models.Task:
    """Créer une nouvelle tâche."""
    task = models.Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/{task_id}", response_model=schemas.TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)) -> models.Task:
    """Récupérer une tâche par son identifiant."""
    task = db.get(models.Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    return task


@router.put("/{task_id}", response_model=schemas.TaskRead)
def update_task(
    task_id: int,
    payload: schemas.TaskUpdate,
    db: Session = Depends(get_db),
) -> models.Task:
    """Mettre à jour partiellement une tâche."""
    task = db.get(models.Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    """Supprimer une tâche."""
    task = db.get(models.Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    db.delete(task)
    db.commit()
