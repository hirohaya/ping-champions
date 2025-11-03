
# Modelo para Event (Evento)
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    date = Column(DateTime, nullable=False)
    time = Column(String(10), nullable=False)
    active = Column(Boolean, default=True)  # Visibility flag (soft delete)
    players = relationship("Player", back_populates="event", cascade="all, delete-orphan")
