from sqlalchemy import Column, Integer, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class MessageChain(Base):
    __tablename__ = "message_chain"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, nullable=False)
    cliente_data = Column(JSON, nullable=False)
    podcast_id = Column(Integer, ForeignKey("podcast.id"), nullable=True)
    vehiculo_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    podcast = relationship("Podcast")