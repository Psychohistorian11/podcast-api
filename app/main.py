from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager
import logging
import time
from fastapi import FastAPI, Request
from app.config import get_settings
from app.database import engine, Base
from app.routers import participant, podcast, episode, chain

settings = get_settings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("podcast-api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API RESTful to manage podcasts, episodes and participants",
    lifespan=lifespan,
)

Instrumentator().instrument(app).expose(app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000
    logger.info(
        f"method={request.method} "
        f"path={request.url.path} "
        f"status={response.status_code} "
        f"duration_ms={duration:.1f}"
    )
    return response

app.include_router(participant.router)
app.include_router(podcast.router)
app.include_router(episode.router)
app.include_router(chain.router)

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