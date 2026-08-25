from fastapi import FastAPI, Depends, HTTPException
from schemas import TaskCreate
from database import Base, engine, SessionLocal
from models import Task as TaskModel
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "hello"}

@app.get("/tasks")
async def show_tasks(db: Session = Depends(get_db)):
    return db.query(TaskModel).all()

@app.post("/tasks")
async def write_tasks(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskModel(title=task.title, done=task.done)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task:
        return task
    raise HTTPException(status_code=404, detail="No task with matching id")

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    existing_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if existing_task:
        existing_task.title = task.title
        existing_task.done = task.done
        db.commit()
        db.refresh(existing_task)
        return existing_task
    raise HTTPException(status_code=404, detail="No task with matching id")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    existing_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if existing_task:
        db.delete(existing_task)
        db.commit()
        return {"message": f"task {task_id} deleted"}
    raise HTTPException(status_code=404, detail="No task with matching id") 
