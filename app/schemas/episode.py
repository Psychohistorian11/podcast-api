from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EpisodeBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_minutes: int
    podcast_id: int
    participant_id: int


class EpisodeCreate(EpisodeBase):
    pass


class EpisodeUpdate(EpisodeBase):
    pass


class EpisodePatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    podcast_id: Optional[int] = None
    participant_id: Optional[int] = None


class EpisodeResponse(EpisodeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True