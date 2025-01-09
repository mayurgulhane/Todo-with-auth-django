from fastapi import FastAPI
from models import models
from db.session import engine
from api.routers import user_router, task_router
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers with prefixes
app.include_router(user_router)
app.include_router(task_router)


app.mount("/static", StaticFiles(directory="frontend"), name="static")