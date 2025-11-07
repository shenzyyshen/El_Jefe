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

#get all goal
    goals = db.query(models.Goal).filter(models.Goal.user_id == user_id).all()

    visible_tasks = []

    for goal in goals:
        goal_tasks= (
            db.query(models.Task)
            .filter(models.Task.goal_id == goal.id, models.Task.completed == False)
            .join(models.Goal, models.Task.goal_id == models.Goal.id)
            .order_by(models.Task.difficulty_stage.asc(), models.Task.id.asc())
            .all()
        )

        if not goal_tasks:
            continue

        #what stage each task is in
        stages_remaining = {t.difficulty_stage for t in goal_tasks}
        current_stage = min(stages_remaining)

        stage_tasks = [t for t in goal_tasks if t.difficulty_stage == current_stage][:5]

        for task in stage_tasks:
            visible_tasks.append((task, goal))



    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "tasks": visible_tasks  #only 5 tasks
    }
)
