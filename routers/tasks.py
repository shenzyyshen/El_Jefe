""" tasks.py
Manages task updates (edit and toggle completion
 Moves tasks between active and finished tasks
 Update progression index """

from fastapi import APIRouter, Depends, HTTPException
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

def update_task(task_id: int, updated_task: schemas.TaskUpdate, db: Session =Depends(get_db)):
    task= db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.description = updated_task.description
    db.commit()
    db.refresh(task)

    return task

"""Toggle tasks completion. 
if completed. move to finished tasks and increment progress
if uncompleted, restore it to active tasks."""
@router.patch("/{task_id}/complete_toggle")
def toggle_task_complete(task_id: int, db: Session=Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    #toggle completion
    task.completed = not task.completed
    db.commit()
    db.refresh(task)

    #if task was completed move to
    if task.completed:

        completed_task = models.CompletedTask(
                user_id=task.goal.user_id,
                title=task.description,
                difficulty=task.difficulty_stage
        )
        db.add(completed_task)

        #updsate users progression index
        user = db.query(models.User).filter(models.User.id == completed_task.user_id).first()
        if user:
            user.progression_index = (user.progression_index or 0) + 1

        #delete active task now that its archived
        db.delete(task)
        db.commit()

        return{
            "task_id": task.id,
            "completed": True,
            "message": "Task Completed and moved to Achievement Log."
        }

    else:
        restored_task =models.Task(
            description=task.description,
            goal_id=task.goal.id,
            difficulty_stage=task.difficulty_stage,
            completed=False
        )
        db.add(restored_task)

        #reduce users progression index
        user = db.query(models.User).filter(models.User.id == task.goal.user_id).first()
        if user and user.progression_index > 0:
            user.progression_index -= 1

        #remove from CompletedTask table
        finished_task = db.query(models.CompletedTask).filter(
            models.CompletedTask.user_id == task.goal.user_id,
            models.CompletedTask.title == task.description
        ).first()
        if finished_task:
            db.delete(finished_task)

        db.commit()
        return {
            "task_id": restored_task.id,
            "completed": False,
            "message": "Task restored to active task"
        }








