

# FastAPI imports for API routing and dependency injection
from fastapi import APIRouter, Depends, HTTPException
# SQLAlchemy imports for database session management
from sqlalchemy.orm import Session
from database import SessionLocal
# Import Match and Player models
from models.match import Match
from models.player import Player
# Import schemas
from schemas import MatchCreate, MatchRead, MatchUpdate

# Router for match-related endpoints
router = APIRouter(prefix="/matches", tags=["matches"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Register a new match in an event
@router.post("/")
def register_match(match_data: MatchCreate, db: Session = Depends(get_db)):
    """Create a new match between two players"""
    # Validate players exist and belong to the event
    player1 = db.query(Player).filter(
        Player.id == match_data.player1_id,
        Player.event_id == match_data.event_id
    ).first()
    
    player2 = db.query(Player).filter(
        Player.id == match_data.player2_id,
        Player.event_id == match_data.event_id
    ).first()
    
    if not player1:
        raise HTTPException(status_code=400, detail="Player 1 not found in event")
    if not player2:
        raise HTTPException(status_code=400, detail="Player 2 not found in event")
    if player1.id == player2.id:
        raise HTTPException(status_code=400, detail="Player cannot play against themselves")
    
    match = Match(
        event_id=match_data.event_id,
        player1_id=match_data.player1_id,
        player2_id=match_data.player2_id,
        best_of=match_data.best_of
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


# List all matches in an event
@router.get("/")
def list_matches(event_id: int, db: Session = Depends(get_db)):
    """Get all matches for an event"""
    return db.query(Match).filter(Match.event_id == event_id).all()


# Get a specific match
@router.get("/{match_id}")
def get_match(match_id: int, db: Session = Depends(get_db)):
    """Get details of a specific match"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


# Update a match (set winner, mark as finished)
@router.put("/{match_id}")
def update_match(match_id: int, match_update: MatchUpdate, db: Session = Depends(get_db)):
    """Update match result (set winner and finish status)"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # If setting a winner, validate it's one of the players
    if match_update.winner_id is not None:
        if match_update.winner_id not in [match.player1_id, match.player2_id]:
            raise HTTPException(
                status_code=400,
                detail="Winner must be one of the match players"
            )
        match.winner_id = match_update.winner_id
    
    if match_update.finished is not None:
        match.finished = match_update.finished
    
    db.commit()
    db.refresh(match)
    return match


# Delete a match
@router.delete("/{match_id}")
def delete_match(match_id: int, db: Session = Depends(get_db)):
    """Delete a match"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    db.delete(match)
    db.commit()
    return {"detail": "Match deleted successfully"}
