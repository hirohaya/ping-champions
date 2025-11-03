

# FastAPI imports for API routing and dependency injection
from fastapi import APIRouter, Depends
from sqlalchemy import func
# SQLAlchemy imports for database session management
from sqlalchemy.orm import Session
from database import SessionLocal
# Import Player and Match models
from models.player import Player
from models.match import Match
# Import schemas
from schemas import RankingEntry

# Router for ranking endpoints
router = APIRouter(prefix="/ranking", tags=["ranking"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get ranking of players in an event based on match wins
@router.get("/")
def event_ranking(event_id: int, db: Session = Depends(get_db)):
    """Get player ranking for an event based on wins/losses"""
    players = db.query(Player).filter(
        Player.event_id == event_id,
        Player.active == 1
    ).all()
    
    ranking_data = []
    
    for player in players:
        # Count wins
        wins = db.query(func.count(Match.id)).filter(
            Match.event_id == event_id,
            Match.winner_id == player.id,
            Match.finished == 1
        ).scalar() or 0
        
        # Count losses
        losses = db.query(func.count(Match.id)).filter(
            Match.event_id == event_id,
            ((Match.player1_id == player.id) | (Match.player2_id == player.id)),
            Match.finished == 1,
            Match.winner_id != player.id
        ).scalar() or 0
        
        total_matches = wins + losses
        win_rate = (wins / total_matches * 100) if total_matches > 0 else 0.0
        
        ranking_data.append({
            "player_id": player.id,
            "name": player.name,
            "wins": wins,
            "losses": losses,
            "win_rate": round(win_rate, 2),
            "total_matches": total_matches
        })
    
    # Sort by wins (desc), then by win_rate (desc)
    ranking_data.sort(key=lambda x: (x["wins"], x["win_rate"]), reverse=True)
    
    # Add position/rank
    for i, entry in enumerate(ranking_data, 1):
        entry["rank"] = i
    
    return ranking_data
