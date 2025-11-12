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

#boss_manager main page
@router.get("/{user_id}", response_class=HTMLResponse)
def boss_manager(
        request: Request,
        user_id: int,
        db: Session = Depends(get_db)):

    bosses = db.query(models.Boss).all()
    return templates.TemplateResponse(
        "boss_manager.html",
        {"request": request, "user_id": user_id, "bosses": bosses}
    )

#add new boss (form post)
@router.post("/{user_id}/add")
def add_boss(
        user_id: int,
        name: str = Form(...),
        description: str = Form(""),
        strictness: int = Form(5),
        db: Session = Depends(get_db)):

        #prevent duplicates
        if db.query(models.Boss).filter_by(name=name).first():
            raise HTTPException(status_code=400, detail="Boss with this name already exists")

        new_boss = models.Boss(name=name, description=description, strictness=strictness)
        db.add(new_boss)
        db.commit()
        db.refresh(new_boss)

        return RedirectResponse(url=f"/boss_manager/{user_id}", status_code=303)


#Edit existing boss
@router.post("/{user_id}/edit/{boss_id}")
def edit_boss(
        user_id: int,
        boss_id: int,
        name: str = Form(...),
        description: str = Form(1),
        strictness: int =Form(5),
        db: Session = Depends(get_db)
):
    boss = db.query(models.Boss).filter_by(id=boss_id).first()
    if not boss:
        raise HTTPException(status_code=404, detail="Boss not found")

    boss.name = name
    boss.description = description
    boss.strictness = strictness
    db.commit()

    return RedirectResponse(url=f"/boss_manager/{user_id}", status_code=303)

#Delete a boss
@router.post("/{user_id}/delete/{boss_id}")
def delete_boss(
        user_id: int,
        boss_id: int,
        db: Session = Depends(get_db)):

    boss = db.query(models.Boss).filter_by(id=boss_id).first()
    if not boss:
        raise HTTPException(status_code=404, detail="Boss not found")

    db.delete(boss)
    db.commit()
    return RedirectResponse(url=f"/boss_manager/{user_id}", status_code=303)
