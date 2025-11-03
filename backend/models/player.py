# Modelo para Player (Jogador)
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, default=0)
    ranking = Column(Integer, default=0)
    active = Column(Integer, default=1)  # 1=active, 0=removed

    event = relationship("Event", back_populates="players", passive_deletes=True)
