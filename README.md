# 🧠 Cereflo API

Une API REST complète pour la gestion de tâches et d'idées — **cereflo** = *cerebrum* (cerveau) + *flow* (flux) : le flux de la pensée organisé en données.

## 🚀 Stack technique

| Technologie | Rôle |
|---|---|
| **Python 3.10+** | Langage principal |
| **FastAPI** | Framework web asynchrone |
| **SQLAlchemy** | ORM (base de données) |
| **SQLite** | Base de données embarquée |
| **Pydantic** | Validation des données |
| **Pytest** | Tests automatisés |
| **Uvicorn** | Serveur ASGI |

## 📦 Installation

```bash
# Cloner le repository
git clone https://github.com/Digital-Wrk/cereflo-api.git
cd cereflo-api

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

## ▶️ Lancer le serveur

```bash
uvicorn app.main:app --reload
```

L'API est disponible sur : http://127.0.0.1:8000
Documentation interactive (Swagger) : http://127.0.0.1:8000/docs

## 🗂️ Endpoints

| Méthode | Route | Description |
|---|---|---|
| GET | `/tasks` | Lister les tâches |
| POST | `/tasks` | Créer une tâche |
| GET | `/tasks/{id}` | Détail d'une tâche |
| PUT | `/tasks/{id}` | Modifier une tâche |
| DELETE | `/tasks/{id}` | Supprimer une tâche |

## 🧪 Tests

```bash
pytest
```

## 🗺️ Roadmap

- [x] CRUD complet des tâches
- [ ] Authentification JWT
- [ ] Projets (regroupement de tâches)
- [ ] Pagination et filtres
- [ ] CI GitHub Actions
- [ ] Déploiement Docker

## 📄 Licence

MIT