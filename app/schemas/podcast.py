from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime


class PodcastBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    language: Optional[str] = "Español"


class PodcastCreate(PodcastBase):
    pass


class PodcastUpdate(PodcastBase):
    pass


class PodcastPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None


class PodcastResponse(PodcastBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    external_data: Optional[Any] = None

    model_config = ConfigDict(from_attributes=True)