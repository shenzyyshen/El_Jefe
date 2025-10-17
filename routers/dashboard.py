""" dashboard.py
display all goals and their associated tasks """


from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
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
    retrieve user info, goals.
    passes data to dashboard.html template"""

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        return HTTPException(status_code=404, detail="user not found")

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "goals": user.goals
    })
