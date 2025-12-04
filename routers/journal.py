from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from core.database import SessionLocal
from routers import models

from services.ai_service import client as ai_client
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/journal", tags=["Journal"])
templates = Jinja2Templates(directory="html")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def journal_history(db: Session, user_id: int):
    return (
            db.query(models.JournalEntry)
            .filter(models.JournalEntry.user_id == user_id)
            .order_by(models.JournalEntry.created_at)
            .all()
    )

#---page routes ----

@router.get("/{user_id}", response_class=HTMLResponse)
def journal_page(
        request: Request,
        user_id: int,
        db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    entries = journal_history(db, user_id)

    return templates.TemplateResponse(
        "journal.html",
        {
            "request":request,
            "user": user,
            "user_id": user_id,
            "entries": entries

        },
    )

#---submit entry----

@router.post("/add", response_class=HTMLResponse)
def add_journal_entry(
        request: Request,
        user_id: int = Form(...),
        content: str = Form(...),
        db: Session = Depends(get_db),
):
    new_entry = models.JournalEntry(
        user_id = user_id,
        content = content
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    try:
        reply = ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages = [
                {"role": "system", "content": "You are my secret diary. Stern, Reflective, Empathetic giving the best real-world advice to help me reach my goals."},
                {"role": "user", "content": content}
            ],
        )
        ai_answer = reply.choices[0].message.content

    #save ai reply
        new_entry.ai_response = reply.choices[0].message.content
        db.commit()
    except Exception as e:
        new_entry.ai_response = f"AI reply failed: {e}"
        db.commit()

    #reload page
    user = db.query(models.User).filter(models.User.id == user_id).first()
    entries = journal_history(db, user_id)

    return templates.TemplateResponse(
        "journal.html",
        {
            "request": request,
            "user": user,
            "user_id": user_id,
            "entries": entries
        }
    )


#----default routes
@router.get("/", response_class=HTMLResponse)
def journal_default(request: Request, db: Session = Depends(get_db)):
    default_user_id = 1

    user = db.query(models.User).filter(models.User.id == default_user_id).first()
    entries = journal_history(db, default_user_id)

    return templates.TemplateResponse(
        "journal.html",
        {
            "request": request,
            "user": user,
            "user_id": default_user_id,
            "entries": entries
        },
    )

#----AI endpoint

@router.post("/{user_id}/ai")
async def journal_ai(user_id: int, request: Request):
    data = await request.json()
    text = data.get("text", "")

    messages = [
        {"role": "system","content":"you are my secret diary. Stern, Reflective, Empathetic giving the best real-world advice to help me reach my goals."},
        {"role": "user", "content": text}
    ]

    reply = ai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages= messages
    )
    ai_text = reply.choices[0].message["content"]

    return{"reply": ai_text}






