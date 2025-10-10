""" dashboard.py
display all goals and their associated tasks """


from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from core import  database
from routers import models

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
templates = Jinja2Templates(directory="templates")

def get_db():
    """Dependency to get DB session
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def dashboard(request: Request,profile_id: int, db: Session = Depends(get_db)):
    """ display dashboard for a specific profile.
    retrieve profile info, goals.
    passes data to dashboard.html template"""

    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()

    if not profile:
        return HTMLResponse("<h1>Profile not found</h1>", status_code=404)

    return templates.TemplateResponse("dashboard.html",{
        "request": request,
        "profile": profile,
        "goals": profile.goals
    })
