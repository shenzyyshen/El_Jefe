""" login.py - unified login and signup
 if username exists - log in
 if username doesn't - save to db
 then redirect to dashboard

"""


from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from core import  database
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


@router.get("/", response_class=HTMLResponse)
def show_login_signup(request: Request):
    """Serve the login/signup page """
    return templates.TemplateResponse("login_signup.html", {"request": request})


@router.post("/auth")
def login_or_signup(
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)):


    """Log in if user exists, otherwise create new user"""
    # strip whitespace
    username = username.strip()
    password = password.strip()

    """login if username exists, otherwise create account"""

    # ensure small passwords won't break bcrypt
    if len(password) > 72:
        password = password[:72]

    #find existing user
    user = db.query(models.User).filter(models.User.username == username).first()

    if user:
     #if user exists, check password
        if not pwd_context.verify(password, user.password):
            raise HTTPException(status_code=404, detail="Incorrect password")
        #redirect to dashboard
        return RedirectResponse(url=f"/dashboard/{user.id}", status_code=303)

    print("🔍 Debugging password before hashing:")
    print(f"  Raw value: {repr(password)}")
    print(f"  Type: {type(password)}")
    print(f"  Length: {len(password)}")

    # otherwise create a new user
    hashed_password = pwd_context.hash(password)
    new_user = models.User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(url=f"/dashboard/{new_user.id}", status_code=303)

