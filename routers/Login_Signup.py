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
from passlib.hash import sha256_crypt
from routers import models


router = APIRouter(prefix="/login_signup", tags=["login_signup"])

templates = Jinja2Templates(directory="html")

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
async def login_or_signup(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)):

    username = username.strip()
    password = password.strip()

    """login if username exists, otherwise create account"""

    print(" Debugging password at start:")
    print(f"  Raw value: {repr(password)}")
    print(f"  Type: {type(password)}")
    print(f"  Length: {len(password)}")

    #find existing user
    user = db.query(models.User).filter(models.User.username == username).first()

    if user:
        if not sha256_crypt.verify(password, user.password):
            raise HTTPException(status_code=404, detail="Incorrect password")
        
        return RedirectResponse(
            url=f"/dashboard/{user.id}", 
            status_code=303)

    # otherwise create a new user
    hashed_password = sha256_crypt.hash(password)
    new_user = models.User(username=username, password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(
        url=f"/dashboard/{new_user.id}", 
        status_code=303
        )

