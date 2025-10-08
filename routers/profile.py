"""
Profile.py
creating and retrieving profiles.
"""
"""

Profile Endpoints

Method	  Endpoint	     Description

POST	/profiles/	      Create a new profile (username, boss persona).
GET	   /profiles/{id}	  Retrieve a profile by ID, including its goals.

"""
from fastapi import FastAPI, APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from routers import models
from core import schemas, database
from sqlalchemy.orm import Session
from services.ai_service import generate_tasks_from_goal
from pydantic import BaseModel
from typing import List
from sqlalchemy.exc import IntegrityError

app=FastAPI()
router = APIRouter(prefix="/profiles", tags=["Profiles"])


class GoalRequest(BaseModel):
    title: str
    boss: str

class ProfileRequest(BaseModel):
    username: str
    goals: list[GoalRequest]


# get db session

def get_db():
    """Dependency function that creates a DB session for each request."""
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


    """ creates a new user profile with one or more goals.
    each goal is saved to the database and can later trigger AI task gen"""
@router.post("/", response_model=schemas.Profile)
def create_profile(request: ProfileRequest, db: Session = Depends(get_db)):


    db_profile = (db.query(models.Profile).filter(models.Profile.username == request.username).first())
    if not db_profile:

        db_profile = models.Profile(username=request.username)
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)

    for goal_data in request.goals:
        db_goal = models.Goal(
            title=goal_data.title,
            boss=goal_data.boss,
            profile_id=db_profile.id
        )
        db.add(db_goal)
        db.commit()
        db.refresh(db_goal)

    return RedirectResponse(
        url=f"/dashboard/{db_profile.id}", status_code=303
    )


@router.get("/{profile_id}", response_model=schemas.Profile)
def read_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Fetch a profile by ID, including its related goals.
    """

    db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile
