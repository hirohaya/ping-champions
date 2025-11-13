# Model for Match
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    player1_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=True)
    best_of = Column(Integer, default=5)
    finished = Column(Boolean, default=False)  # Match completion status
    
    # Game scores (e.g., "11-9,10-12,11-8,11-6" or "11-9 11-8 11-6")
    player1_games = Column(Integer, default=0)  # Number of games won by player 1
    player2_games = Column(Integer, default=0)  # Number of games won by player 2
    games_score = Column(String, nullable=True)  # Detailed score per game (e.g., "11-9,10-12,11-8")

    event = relationship("Event", back_populates="matches")
    tournament = relationship("Tournament", back_populates="matches")
    player1 = relationship("Player", foreign_keys=[player1_id], back_populates="matches_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_id], back_populates="matches_as_player2")
    winner = relationship("Player", foreign_keys=[winner_id])
