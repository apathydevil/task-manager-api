from fastapi import FastAPI
from fastapi import HTTPException
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

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="No task with matching id")

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: TaskCreate):
    for existing_task in tasks:
        if existing_task.id == task_id:
            existing_task.title = task.title
            existing_task.done = task.done
            return existing_task
    raise HTTPException(status_code=404, detail="No task with matching id")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for existing_task in tasks:
        if existing_task.id == task_id:
            tasks.remove(existing_task)
            return {"message": f"task {task_id} deleted"}
    raise HTTPException(status_code=404, detail="No task with matching id")      