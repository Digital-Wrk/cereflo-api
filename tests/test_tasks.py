"""Tests du CRUD des tâches — exécutés avec pytest."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.deps import get_db
from app.main import app


# Base SQLite en mémoire, isolée pour les tests
TEST_DB_URL = "sqlite://"

test_engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture()
def client():
    """Client de test avec base de données isolée."""
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


class TestCreateTask:
    def test_create_task_returns_201(self, client):
        resp = client.post("/tasks", json={"title": "Apprendre FastAPI"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["id"] == 1
        assert data["title"] == "Apprendre FastAPI"
        assert data["done"] is False

    def test_create_task_empty_title_rejected(self, client):
        resp = client.post("/tasks", json={"title": ""})
        assert resp.status_code == 422


class TestListTasks:
    def test_list_empty(self, client):
        resp = client.get("/tasks")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_returns_created_tasks(self, client):
        client.post("/tasks", json={"title": "Tâche 1"})
        client.post("/tasks", json={"title": "Tâche 2"})
        resp = client.get("/tasks")
        assert len(resp.json()) == 2

    def test_filter_by_done(self, client):
        client.post("/tasks", json={"title": "À faire", "done": False})
        client.post("/tasks", json={"title": "Terminée", "done": True})
        resp = client.get("/tasks", params={"done": True})
        data = resp.json()
        assert len(data) == 1
        assert data[0]["title"] == "Terminée"


class TestGetTask:
    def test_get_existing_task(self, client):
        created = client.post("/tasks", json={"title": "Lire"}).json()
        resp = client.get(f"/tasks/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Lire"

    def test_get_missing_task_returns_404(self, client):
        resp = client.get("/tasks/999")
        assert resp.status_code == 404


class TestUpdateTask:
    def test_partial_update(self, client):
        created = client.post("/tasks", json={"title": "Avant"}).json()
        resp = client.put(f"/tasks/{created['id']}", json={"done": True})
        assert resp.status_code == 200
        data = resp.json()
        assert data["done"] is True
        assert data["title"] == "Avant"  # non modifié

    def test_update_missing_returns_404(self, client):
        resp = client.put("/tasks/999", json={"done": True})
        assert resp.status_code == 404


class TestDeleteTask:
    def test_delete_returns_204_then_404(self, client):
        created = client.post("/tasks", json={"title": "Temporaire"}).json()
        resp = client.delete(f"/tasks/{created['id']}")
        assert resp.status_code == 204
        assert client.get(f"/tasks/{created['id']}").status_code == 404

    def test_delete_missing_returns_404(self, client):
        assert client.delete("/tasks/999").status_code == 404


class TestHealth:
    def test_health_check(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}
