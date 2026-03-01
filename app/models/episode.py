from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Episode(Base):
    __tablename__ = "episode"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    podcast_id = Column(Integer, ForeignKey("podcast.id"), nullable=False)
    participant_id = Column(Integer, ForeignKey("participant.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    podcast = relationship("Podcast", back_populates="episode")
    participant = relationship("Participant", back_populates="episode")