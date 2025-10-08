""" dashboard.py
display all goals and their associated tasks """


from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import models
from core import  database
from sqlalchemy.orm import Session

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

templates = Jinja2Templates(directory="templates")

def get_db():
    """Dependecy to get DB session
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def dashboard(request: Request, profile_id: int, db: Session = Depends(get_db)):
    """ display dashboard for a specific profile.
    retrieve profile info, goals.
    passes data to dashboard.html template"""

    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "profile": profile}
    )
