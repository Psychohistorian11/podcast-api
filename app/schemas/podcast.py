from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PodcastBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    language: Optional[str] = "Español"


class PodcastCreate(PodcastBase):
    pass


class PodcastUpdate(PodcastBase):
    """Para PUT - todos los campos requeridos."""
    pass


class PodcastPatch(BaseModel):
    """Para PATCH - todos los campos opcionales."""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None


class PodcastResponse(PodcastBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True