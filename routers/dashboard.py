""" dashboard.py
display all goals and their associated tasks """


from fastapi import APIRouter, Depends, Body, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from core import  database
from routers import models

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
templates = Jinja2Templates(directory="html")

def get_db():
    """Dependency to get DB session
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{user_id}", response_class=HTMLResponse)
def dashboard(request: Request, user_id: int, db: Session = Depends(get_db)):
    """ display dashboard for a specific user.
    retrieve user info, goals and tasks
    displays tasks of the goals retirved.
    passes data to dashboard.html template"""

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    #get tasks of goals
    tasks_with_goals = (
        db.query(models.Task, models.Goal)
        .join(models.Goal, models.Task.goal_id == models.Goal.id)
        .filter(models.Goal.user_id == user_id)
        .filter(models.Task.completed == False)
        .order_by(models.Task.difficulty_stage.asc(), models.Task.id.asc())
        .all()
    )

    stages = [t.difficulty_stage for t, g in tasks_with_goals if t.difficulty_stage is not None]
    current_stage = min(stages) if stages else 0

    visible_tasks =[(t, g) for (t, g) in tasks_with_goals if t.difficulty_stage == current_stage][:5]

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "tasks": visible_tasks  #only 5 tasks
    }
)
