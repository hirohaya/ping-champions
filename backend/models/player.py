# Modelo para Player (Jogador)
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    elo_rating = Column(Float, default=1200.0)  # Elo rating starts at 1200 (from REFINAMENTO_FEATURE_1.md)
    score = Column(Integer, default=0)  # Legacy: number of wins
    ranking = Column(Integer, default=0)  # Position in tournament ranking
    active = Column(Boolean, default=True)  # Soft delete flag

    event = relationship("Event", back_populates="players", passive_deletes=True)
    matches_as_player1 = relationship("Match", foreign_keys="Match.player1_id", back_populates="player1")
    matches_as_player2 = relationship("Match", foreign_keys="Match.player2_id", back_populates="player2")
    memberships = relationship("Membership", back_populates="player", cascade="all, delete-orphan")
