from fastapi import FastAPI
from models import Task, TaskCreate

tasks = [Task(id=1, title = "test")]

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "hello"}

@app.get("/tasks")
async def show_tasks():
    return tasks

@app.post("/tasks")
async def write_tasks(task: TaskCreate):
    new_task = Task(id=len(tasks) + 1, title=task.title, done=task.done)
    tasks.append(new_task)
    return new_task