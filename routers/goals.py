
"""
goals.py
Reltaed to creating and retrieving goals.
"""
"""
Method	   Endpoint	             Description
POST   	/goals/{profile_id}	     Create a goal linked to a profile.
GET	    /goals/{profile_id}	     Retrieve all goals for a profile.
"""


from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from core import schemas
from routers import models
from services import ai_service
from pydantic import BaseModel

router = APIRouter(prefix="/goals", tags=["Goals"])

class GoalCreateRequest(BaseModel):
    title:str
    description: str = ""
    boss: str = "default"


#______________________________________________________
def get_db():
    """Provide a database session to path operations"""
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

#_________________________________________________________
@router.post("/{profile_id}", response_model=schemas.Goal)
def elaborate_goal(
        profile_id: int,
        title: str = Form(...),
        description: str = Form(None),
        db: Session = Depends(get_db)):
    """
   saves goal for a given profile.
    -uses profile_id to link goal to correct user.
    -calls ai to generate tasks form this goal
    """

    db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    """ save goal"""
    db_goal = models.Goal(
        title=title,
        description=description,
        profile_id=db_profile.id
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)

    """call ai to generate task from goals"""
    ai_tasks = generate_tasks_from_goal(title, db)

    for task in ai_tasks:
        db_task = models.Task(description=task, goal_id=db_goal.id)
        db.add(db_task)
    db.commit()

    return {
        "id": db_goal.id,
        "title": db_goal.title,
        "description": db_goal.description,
        "boss": db_goal.boss,
        "tasks": ai_tasks
    }

#__________________________________________________
@router.get("/{profile_id}", response_model=list[schemas.Goal])
def read_goals(profile_id: int, db: Session = Depends(get_db)):
    """
    Get all goals for a given profile
    """
    return db.query(models.Goal).filter(models.Goal.profile_id == profile_id).all()

#_____________________________________________________

