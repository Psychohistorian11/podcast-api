from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Participant(Base):
    __tablename__ = "participant"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    role = Column(String(50), nullable=False)
    bio = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación: un participante puede estar en muchos episodios
    episodes = relationship("Episode", back_populates="participant")