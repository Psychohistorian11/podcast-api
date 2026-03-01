from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ParticipantBase(BaseModel):
    name: str
    email: str
    role: str
    bio: Optional[str] = None


class ParticipantCreate(ParticipantBase):
    pass


class ParticipantUpdate(ParticipantBase):
    pass


class ParticipantPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    bio: Optional[str] = None


class ParticipantResponse(ParticipantBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True