from fastapi import FastAPI

app = FastAPI(
    title="podcast-api",
    version="0.1.0",
    description="API RESTful sencilla para la gestión de podcasts",
)


@app.get("/", tags=["Health"])
def root():
    return {"status": "running", "app": "podcast-api", "version": "0.1.0"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}