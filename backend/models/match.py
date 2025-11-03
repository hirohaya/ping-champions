# Model for Match
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    player1_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    best_of = Column(Integer, default=5)
    finished = Column(Boolean, default=False)  # Match completion status

    event = relationship("Event", back_populates="matches")
    player1 = relationship("Player", foreign_keys=[player1_id], back_populates="matches_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_id], back_populates="matches_as_player2")
    winner = relationship("Player", foreign_keys=[winner_id])
