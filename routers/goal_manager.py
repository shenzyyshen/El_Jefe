"""
goal_management.py
Manage user's goals:
- Add new goals
- Edit existing goals
- Delete goals
- Mark goals complete
- Display all goals (active + completed)
"""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, selectinload
from core import database
from routers import models
from services import ai_service

router = APIRouter(prefix="/goal_manager", tags=["Goal Manager"])
templates = Jinja2Templates(directory="html")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{user_id}", response_class=HTMLResponse)
def show_goal_manager(user_id: int, request: Request, db: Session = Depends(get_db)):
    """display goal manager page for user W/ task loaded"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return HTMLResponse("user not found", status_code=404)

    goals = (
        db.query(models.Goal).filter(models.Goal.user_id == user.id).all()
    return templates.TemplateResponse(
        "goal_manager.html",
        {"request": request, "user": user, "goals": goals}
    )

@router.post("/{user_id}/add")
def add_goal(user_id: int, title: str = Form(...), description: str = Form(None), db: Session = Depends(get_db)):
    """add a new goal and automatically generate ai tasks"""
    user = db.query(models.User).filter(models.User.id ==user_id).first()
    if not user:
        return HTMLResponse("User not found", status_code=404)

    new_goal = models.Goal(
        title=title,
        description=description,
        user_id=user_id
    )
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    try:
        ai_service.generate_tasks_from_goal(new_goal, db)
    except Exception as e:
        print("AI task generation failed:", e)

    return RedirectResponse(url=f"/goal_manager/{user_id}", status_code=303)


@router.post("/{user_id}/edit/{goal_id}")
def edit_goal(user_id: int, goal_id: int, title: str =Form(...), description: str = Form(None), db: Session = Depends(get_db)):
    goal = db.query(models.Goal).filter(models.Goal.id ==goal_id, models.Goal.user_id == user_id).first()
    if goal:
        goal.title= title
        goal.description = description
        db.commit()
    return RedirectResponse(url=f"/goal_manager/{user_id}", status_code=303)

@router.post("/{user_id}/complete/{goal_id}")
def complete_goal(user_id: int, goal_id: int, title: str =Form(...), description: str = Form(None), db: Session = Depends(get_db)):
    goal = db.query(models.Goal).filter(models.Goal.id == goal_id, models.Goal.user_id == user_id).first()
    if goal:
        goal.completed= True
        db.commit()
    return RedirectResponse(url=f"/goal_manager/{user_id}", status_code=303)

@router.post("/{user_id}/delete/{goal_id}")
def delete_goal(user_id: int, goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if goal:
        db.delete(goal)
        db.commit()
    return RedirectResponse(url=f"/goal_manager/{user_id}", status_code=303)
