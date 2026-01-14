# El Jefe 

El Jefe is a FastAPI-powered productivity and journaling app that combines **goals**, **tasks**, **boss personas**, and an **AI journal companion** to help users reflect, stay motivated, and make progress.

---

##  Features

* User authentication (login / signup)
* Goals with associated tasks
* Boss personas that flavor task generation
* Journal entries with short, friendly AI responses
* AI understands user goals, tasks, and progress
* Clean FastAPI + SQLAlchemy architecture

---

## Tech Stack

* **Python** 3.11–3.13
* **FastAPI**
* **SQLAlchemy**
* **Jinja2** (HTML templates)
* **SQLite** (default DB)
* **OpenAI API** (chat completions)
* **Passlib + bcrypt** (password hashing)

---

## 📁 Project Structure

el-jefe/
│
├── core/
│   ├── config.py          # App configuration & environment settings
│   ├── database.py        # SQLAlchemy engine, session, and DB setup
│   └── schemas.py         # Pydantic schemas
│
├── html/
│   ├── boss_manager.html
│   ├── dashboard.html
│   ├── finished_tasks.html
│   ├── goal_manager.html
│   ├── journal.html
│   ├── login_signup.html
│   └── profile.html
│
├── routers/
│   ├── __init__.py
│   ├── boss_manager.py    # Boss logic & routing
│   ├── dashboard.py       # Dashboard routes
│   ├── goal_manager.py    # Goal creation & management
│   ├── goals.py           # Goal-related logic
│   ├── journal.py         # Journal + AI responses
│   ├── login_signup.py    # Authentication routes
│   ├── models.py          # SQLAlchemy models
│   ├── profile.py         # User profile routes
│   └── tasks.py           # Task management routes
│
├── services/
│   ├── __init__.py
│   ├── ai_service.py      # OpenAI interaction & AI logic
│   └── progression.py    # Goal/task progression logic
│
├── .env                   # Environment variables (not committed)
├── .gitignore             # Git ignore rules
├── eljefe.db              # SQLite database
├── init_db.py             # Database initialization
├── main.py                # FastAPI app entry point
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation



---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

---

## 🐍 Python Virtual Environment (REQUIRED)

**macOS / Linux**

```bash
cd "el jefe"
python3 -m venv .venv
source .venv/bin/activate
```

Confirm:

```bash
which python
# should point to .venv/bin/python
```

---

## 📦 Install Dependencies

Create a `requirements.txt` with the following:

```
fastapi
uvicorn
sqlalchemy
python-dotenv
jinja2
passlib
bcrypt<4
openai
```

Then install:

```bash
pip install -r requirements.txt
```

> ⚠️ Important: `bcrypt<4` is required for compatibility with `passlib`

---

## 🗄 Initialize Database

```bash
python init_db.py
```

---

## ▶️ Run the App

```bash
uvicorn main:app --reload
```

Open in browser:

👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🤖 AI Behavior

### Journal AI

* Short (2–4 sentences)
* Friendly and conversational
* Reflects emotions
* Connects journal entries to goals & tasks
* Gives **one actionable suggestion**

### Task Generation AI

* Generates 15 tasks per goal
* 3 difficulty stages
* Boss personality applied

---

## 🔑 Password Notes (bcrypt)

* Passwords are truncated to 72 characters before hashing
* Required due to bcrypt limitations

---

## 🛠 Common Issues

### `ModuleNotFoundError: passlib`

Ensure:

```bash
pip install passlib bcrypt<4
```

And that `.venv` is activated.

---

### `Address already in use`

Stop existing server:

```bash
lsof -i :8000
kill -9 <PID>
```

---

## 🧠 Future Ideas

* Chat-style journal UI
* Side quests from bosses
* Progress-aware encouragement
* Weekly reflection summaries

---

## ❤️ Credits

Built by Shenzymay

AI powered by OpenAI

