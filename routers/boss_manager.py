from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from core import database
from routers import models

router = APIRouter(prefix="/boss_manager", tags=["Boss Manager"])
templates = Jinja2Templates(directory="html")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#list bosses
@router.get("/", response_class=HTMLResponse)
def list_bosses(request: Request, db: Session = Depends(get_db)):
    bosses = db.query(models.Boss).all()
    return templates.TemplateResponse(
        "boss_manager.html",
        {"request": request, "bosses": bosses}
    )

#add a new boss
@router.post("/add")
def add_boss(
        name: str = Form(...),
        description: str = Form(""),
        strictness: int = Form(1),
        db: Session = Depends(get_db)
):
    if db.query(models.Boss).filter_by(name=name).first():
        raise HTTPException(status_code=400, detail="Boss with this name already exists")

    new_boss = models.Boss(name=name, description=description, strictness=strictness)
    db.add(new_boss)
    db.commit()
    db.refresh(new_boss)
    return RedirectResponse(url="/boss_manage/", status_code=303)

#edit existing boss
@router.post("/edit/{boss_id}")
def edit_boss(
        boss_id: int,
        name: str = Form(...),
        description: str = Form(1),
        db: Session = Depends(get_db)
):
    boss = db.query(models.Boss).filter_by(id=boss_id).first()
    if not boss:
        raise HTTPException(status_code=404, detail="Boss not found")

    boss.name = name
    boss.description = description
    boss.strictness = strictness
    db.commit()
    return RedirectResponse(url="/boss_manager/", status_code=303)

#delete a boss
@router.post("/delete/{boss_id}")
def delete_boss(boss_id: int, db: Session = Depends(get_db)):
    boss = db.query(models.Boss).filter_by(id=boss_id).first()
    if not boss:
        raise HTTPException(status_code=404, detail="Boss not found")

    db.delete(boss)
    db.commit()
    return RedirectResponse(url="/boss_manager/", status_code=303)
