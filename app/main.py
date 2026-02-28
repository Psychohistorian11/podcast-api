from fastapi import FastAPI
from app.config import get_settings
from app.database import engine, Base
from app.models import Participant, Podcast, Episode

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API RESTful to manage podcasts, episodes and participants",
)

# Crear tablas al iniciar
Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "running",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}