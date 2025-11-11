

# FastAPI imports for API routing and dependency injection
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func

# SQLAlchemy imports for database session management
from sqlalchemy.orm import Session

from database import SessionLocal
from models.event import Event
from models.match import Match

# Import Player and Match models
from models.player import Player

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
@router.get("", response_model=list[RankingEntry])
def event_ranking(event_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    """
    Get player ranking for an event based on wins/losses.

    - **event_id**: Event ID to get ranking for (query parameter)

    Returns players sorted by wins (descending) then by win rate (descending)
    """
    return _get_ranking_data(event_id, db)


# Alternative route: Get ranking using path parameter
@router.get("/{event_id}", response_model=list[RankingEntry])
def event_ranking_path(event_id: int, db: Session = Depends(get_db)):
    """
    Get player ranking for an event based on wins/losses (alternative route with path parameter).

    - **event_id**: Event ID to get ranking for (path parameter)

    Returns players sorted by wins (descending) then by win rate (descending)
    """
    return _get_ranking_data(event_id, db)


def _get_ranking_data(event_id: int, db: Session):
    """Helper function to get ranking data"""
    # Verify event exists (active or inactive)
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    players = db.query(Player).filter(
        Player.event_id == event_id,
        Player.active
    ).all()

    ranking_data = []

    for player in players:
        # Count wins
        wins = db.query(func.count(Match.id)).filter(
            Match.event_id == event_id,
            Match.winner_id == player.id,
            Match.finished
        ).scalar() or 0

        # Count losses
        losses = db.query(func.count(Match.id)).filter(
            Match.event_id == event_id,
            ((Match.player1_id == player.id) | (Match.player2_id == player.id)),
            Match.finished,
            Match.winner_id != player.id
        ).scalar() or 0

        total_matches = wins + losses
        win_rate = (wins / total_matches) if total_matches > 0 else 0.0

        ranking_data.append(RankingEntry(
            player_id=player.id,
            name=player.name,
            elo=player.elo_rating,
            wins=wins,
            losses=losses,
            win_rate=round(win_rate, 2)
        ))

    # Sort by wins (desc), then by win_rate (desc)
    ranking_data.sort(key=lambda x: (x.wins, x.win_rate), reverse=True)

    return ranking_data

