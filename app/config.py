from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "podcast-api"
    APP_VERSION: str = "3.0.0"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/podcast_db"
    SIMON_API_URL: str = "http://34.41.107.90"
    JOSE_PABLO_API_URL: str = "http://34.21.77.119/api/v2"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()