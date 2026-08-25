from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    done: bool = False