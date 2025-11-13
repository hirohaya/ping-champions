
# Modelo para Event (Evento)
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    date = Column(String(10), nullable=False)  # Store as string (YYYY-MM-DD format)
    time = Column(String(10), nullable=False)
    active = Column(Boolean, default=True)  # Visibility flag (soft delete)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    players = relationship("Player", back_populates="event", cascade="all, delete-orphan")
    matches = relationship("Match", back_populates="event", cascade="all, delete-orphan")
    memberships = relationship("Membership", back_populates="event", cascade="all, delete-orphan")
    tournaments = relationship("Tournament", back_populates="event", cascade="all, delete-orphan")
