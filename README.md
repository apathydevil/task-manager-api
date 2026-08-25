# task-manager-api

A small CRUD API for managing tasks, built with FastAPI and SQLAlchemy, backed by SQLite.

Built as a hands-on backend learning project. First time writing a server/API, 
first time using an ORM, first time using dependency injection for database sessions.

## Stack

- **FastAPI** — routing, request/response validation
- **SQLAlchemy 2.0** (ORM) — `Mapped[]` / `mapped_column()` style models
- **SQLite** — file-based storage (`tasks.db`, created automatically on first run)
- **Pydantic** — request/response schemas

## Setup

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be running at `http://127.0.0.1:8000`. Interactive docs (Swagger UI) are
available at `http://127.0.0.1:8000/docs`.

## Endpoints

| Method | Path            | Description             |
|--------|-----------------|--------------------------|
| GET    | `/tasks`        | List all tasks           |
| POST   | `/tasks`        | Create a new task        |
| GET    | `/tasks/{id}`   | Get a single task by id  |
| PUT    | `/tasks/{id}`   | Update a task by id      |
| DELETE | `/tasks/{id}`   | Delete a task by id      |

### Task shape

```json
{
  "id": 1,
  "title": "Buy milk",
  "done": false
}
```

`title` is required. `done` defaults to `false`. `id` increments automatically.
