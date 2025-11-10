# Modelo para Player (Jogador)
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, default=0)
    ranking = Column(Integer, default=0)
    active = Column(Boolean, default=True)  # Soft delete flag

    event = relationship("Event", back_populates="players", passive_deletes=True)
    matches_as_player1 = relationship("Match", foreign_keys="Match.player1_id", back_populates="player1")
    matches_as_player2 = relationship("Match", foreign_keys="Match.player2_id", back_populates="player2")
