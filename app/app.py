# app.py
# arranque FastAPI

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes.pages import router as pages_router
from app.routes.chat import router as chat_router
from app.routes.upload import router as upload_router
from app.routes.chat import router as chat_router
from app.routes.upload import router as upload_router

app = FastAPI(title="Assistente de Documentos")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(pages_router)
app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(upload_router)
