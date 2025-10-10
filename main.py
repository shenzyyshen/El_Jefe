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
from core import database
from routers import models, profile, goals, dashboard

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
app.include_router(profile.router)
app.include_router(goals.router)
app.include_router(dashboard.router)

"""
Root Route
"""
@app.get("/")#
def read_root(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})



