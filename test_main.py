from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_read_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200

def test_create_task():
    response = client.post("/tasks", json={"title": "test task"})
    assert response.status_code == 201

def test_get_by_id_impossible():
    response = client.get("/tasks/999999999")
    assert response.status_code == 404

def test_update_task():
    create_response = client.post("/tasks", json={"title": "test task"})
    task_id = create_response.json()["id"]

    new_task = client.put(f"/tasks/{task_id}", json={"title":"updated test task"})
    assert new_task.status_code == 200
    assert new_task.json()["title"] == "updated test task"

def test_delete_task():
    create_response = client.post("/tasks", json={"title": "test task"})
    task_id = create_response.json()["id"]

    delete = client.delete(f"/tasks/{task_id}")
    assert delete.status_code == 200
    assert delete.json() == {"message": f"task {task_id} deleted"}
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

def test_post_no_title():
    response = client.post("/tasks", json={})
    assert response.status_code == 422

def test_put_nonexistent_id():
    response = client.put("/tasks/999999999", json={"title": "updated test task"})
    assert response.status_code == 404

def test_delete_nonexistent_id():
    response = client.delete("/tasks/999999999")
    assert response.status_code == 404