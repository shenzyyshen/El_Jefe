""" tasks.py manages task updates (edit and complete """

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import SessionLocal, Base, engine
from core import schemas
from routers import models

router = APIRouter(prefix="/tasks", tags=["Tasks"])


"""Dependency function that creates a DB session for each request."""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def update_task(
        task_id: int,
        updated_task: schemas.TaskUpdate,
        db: Session =Depends(get_db)):

    task= db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.description =updated_task.description
    db.commit()
    db.refresh(task)
    return task

@router.patch("/{task_id}/complete", response_model=schemas.Task)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task =db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return {"error": "Task not found"}
    task.completed = not task.completed
    db.commit()
    return {"task_id": task.id, "completed": task.completed}

@router.patch("/tasks/{task_id}/complete_toggle")
def toggle_task_complete(task_id: int, db: Session=Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return {"error": "Task not found"}

    #toggle completion
    task.completed = not task.completed
    db.commit()
    db.refresh(task)
    return {"task_id": task.id, "completed": task.completed}









