
# FastAPI imports for API routing and dependency injection
from fastapi import APIRouter, Depends, HTTPException
# SQLAlchemy imports for database session management
from sqlalchemy.orm import Session
from database import SessionLocal
# Import Match model
from models.match import Match

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
def register_match(event_id: int, player1_id: int, player2_id: int, db: Session = Depends(get_db)):
    match = Match(event_id=event_id, player1_id=player1_id, player2_id=player2_id)
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


# List all matches in an event
@router.get("/")
def list_matches(event_id: int, db: Session = Depends(get_db)):
    return db.query(Match).filter(Match.event_id == event_id).all()
