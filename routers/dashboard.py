""" dashboard.py
display all goals and their associated tasks """


from fastapi import APIRouter, Depends, Body, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from core import  database
from routers import models
from services import progression as progression_service

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

    goals = db.query(models.Goal).filter(models.Goal.user_id == user_id).all()
    visible_tasks = []

    for goal in goals:
        goal_tasks= (
            db.query(models.Task)
            .filter(models.Task.goal_id == goal.id, models.Task.completed == False)
            .order_by(models.Task.difficulty_stage.asc(), models.Task.id.asc())
            .all()
        )

        if not goal_tasks:
            continue

        #Only show the lowest difficulty stage tasks (max 5)
        stages_present = {t.difficulty_stage for t in goal_tasks}
        current_stage = min(stages_present)
        stage_tasks = [t for t in goal_tasks if t.difficulty_stage == current_stage][:5]

        for task in stage_tasks:
            visible_tasks.append((task, goal))

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "tasks": visible_tasks
    }
)

""" Marks the progresssion task as completed and stores it in finished task table"""
@router.post("/complete/{user_id}")
def complete_progression_task(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException( status_code=404, detail="User not found")

    idx = user.progression_index or 0
    title = progression_service.get_task_for_index(idx)
    difficulty = idx + 1

    #record completed task
    completed = models.CompletedTask(
        user_id=user.id,
        title=title,
        difficulty=difficulty
    )
    db.add(completed)

    #advance progression index
    user.progression_index = idx + 1
    db.commit()

    return RedirectResponse(url=f"/dashboard/{user.id}", status_code=303)

"""show all finished task (completed) for a user
orderd by most recently completed first"""
@router.get("/finished_tasks/{user_id}", response_class=HTMLResponse)
def finished_tasks(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException( status_code=404, detail="User not found")

    completed_tasks =(
        db.query(models.CompletedTask)
        .filter(models.CompletedTask.user_id ==user.id)
        .order_by(models.CompletedTask.completed_at.desc())
        .all()
    )

    goals= db.query(models.Task).filter(models.Task.goal_id == user.id
        ).order_by(models.Task.difficulty_stage.asc()).all()


    return templates.TemplateResponse(
        "finished_tasks.html",
        {
            "request": request,
            "user": user,
            "completed_tasks": completed_tasks
        }
    )