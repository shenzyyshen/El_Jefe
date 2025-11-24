"""
Boss AI - main application entry point
central hub for fast api applications

- creates the fast api instances
- connects to the databse
- mounts static files (html)
includes routers for authentic, profile managment.
- includes dashboard
- defines settigns

- add AI endpoints
        - goals
        - task
        -journal
        -boss chat
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from core import database
from routers import models, login_signup, goal_manager, dashboard, tasks, boss_manager


"""
DB Table 
"""
models.Base.metadata.create_all(bind=database.engine)

"""FastAPI
"""
app = FastAPI(title="Boss AI")

"""Static + templates
"""
app.mount("/static", StaticFiles(directory="html"), name="static")
templates = Jinja2Templates(directory="html")

"""
Routers
"""
app.include_router(login_signup.router)
app.include_router(goal_manager.router)
app.include_router(dashboard.router)
app.include_router(tasks.router)

app.include_router(boss_manager.router)



"""
Root Route
"""
@app.get("/", response_class=RedirectResponse)
def read_root(request: Request):
    return templates.TemplateResponse("login_signup.html", {"request": request})



