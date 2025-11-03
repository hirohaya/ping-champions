
# FastAPI imports for API routing and dependency injection
from fastapi import APIRouter, Depends
# SQLAlchemy imports for database session management
from sqlalchemy.orm import Session
from database import SessionLocal
# Import Player model
from models.player import Player

# Router for ranking endpoints
router = APIRouter(prefix="/ranking", tags=["ranking"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get ranking of players in an event, ordered by score
@router.get("/")
def event_ranking(event_id: int, db: Session = Depends(get_db)):
    return db.query(Player).filter(Player.event_id == event_id).order_by(Player.score.desc()).all()
