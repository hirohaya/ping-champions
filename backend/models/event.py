
# Modelo para Event (Evento)
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    date = Column(String(10), nullable=False)  # Store as string (YYYY-MM-DD format)
    time = Column(String(10), nullable=False)
    active = Column(Boolean, default=True)  # Visibility flag (soft delete)
    created_at = Column(DateTime, default=datetime.utcnow)
    players = relationship("Player", back_populates="event", cascade="all, delete-orphan")
