""" login.py - unified login and signup
 if username exists - log in
 if username doesn't - save to db
 then redirect to dashboard

"""


from fastapi import FastAPI, APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from core import schemas, database
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from routers import models


router =APIRouter(prefix="/login_signup", tags=["login_signup"])

templates = Jinja2Templates(directory="html")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/auth")
def login_or_signup(
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)):

    """login if username exists, otherwise create account"""

    user = db.query(models.User).filter(models.User.username == username).first()

    if user:
     #if user exists, check password
        if not pwd_context.verify(password, user.password):
            raise HTTPException(status_code=404, detail="Incorrect password")
        #redirect to dashboard
        return RedirectResponse(url=f"/dashboard/{user.id}", status_code=303)

    # otherwise create a new user
    hashed_password = pwd_context.hash(password)
    new_user = models.User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(url=f"/dashboard/{new_user.id}", status_code=303)

@router.get("/login_signup", response_class=HTMLResponse)
def show_login_signup(request: Request):
    """Serve the login/signup page """
    return templates.TemplateResponse("login_signup.html", {"request": request})




