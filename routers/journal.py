from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from sqlalchemy.orm import Session
from core.database import SessionLocal
from routers import models

router = APIRouter(prefix="/journal", tags=["Journal"])
templates = Jinja2Templates(directory="html")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def detect_related_goal_task(db: Session, text: str):
    text_lower = text.lower()
    goal = db.query(models.Goal).filter(models.Goal.title.ilike(f"%{text_lower}%")).first()
    task = db.query(models.Task).filter(models.Task.description.ilike(f"%{text_lower}%")).first()
    return goal, task


def boss_response(goal, task, boss, entry_text: str):
    name=boss.name if boss else "Your Boss"

    if task:
        return (
            f"{name}: Your making progress on '{goal.goal_name}'."
            f"What is the next action you can take on it, that feels achievable?"
        )
    if goal:
        return (
            f"{name}: your making progress on ' {goal.goal_name}'."
            f"What part feels like the hardest right now ?"
        )
    return f"{name}: I hear you. Tell me more."



def write_journal_entry(content: str, db: Session = Depends(get_db)):
    user_id = 1
    goal, task = detect_related_goal_task(db, content)

    if goal:
        boss = db.query(models.Boss).filter(models.Boss.id == goal.boss_id).first()
    elif task:
        goal = db.query(models.Goal).filter(models.Goal.id == task.goal_id).first()
        boss = db.query(models.Boss).filter(models.Boss.id == goal.boss_id).first()
    else:
        boss = db.query(models.Boss).first()

    ai_reply = boss_response(goal, task, boss, content)

    entry = models.JournalEntry(
        user_id=user_id,
        content=content,
        related_goal_id=goal.id if goal else None,
        related_task_id=task.id if task else None,
        assigned_boss_id=boss.id if boss else None,
        ai_response=ai_reply,
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def journal_history(db: Session):
    return db.query(models.JournalEntry).order_by(models.JournalEntry.created_at).all()

#routes
@router.get("/", response_class=HTMLResponse)
def journal_default(request: Request, db: Session = Depends(get_db)):
    default_user_id = 1
    entries = journal_history(db)
    return templates.TemplateResponse(
        "journal.html",
        {"request": request, "user_id": default_user_id, "entries": entries}
    )

@router.get("/{user_id}", response_class=HTMLResponse)
def journal_page(request: Request, user_id: int, db: Session= Depends(get_db)):
    entries = journal_history(db)
    return templates.TemplateResponse(
        "journal.html",
        {"request":request, "user_id": user_id, "entries": entries}
    )

@router.post("/{user_id}/add", response_class=HTMLResponse)
def add_journal_entry(request:Request, user_id: int, entry_text: str = Form(...), db: Session = Depends(get_db)):
    write_journal_entry(entry_text, db)
    entries = journal_history(db)
    return templates.TemplateResponse(
        "journal.html",
        {"request": request, "user_id": user_id, "entries": entries}
    )







