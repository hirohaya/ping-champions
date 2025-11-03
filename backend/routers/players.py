# FastAPI imports for API routing and dependency injection
from fastapi import APIRouter, Depends, HTTPException
# SQLAlchemy imports for database session management
from sqlalchemy.orm import Session
from database import SessionLocal
# Import models
from models.event import Event
from models.player import Player
from models.match import Match

# Router for player-related endpoints
router = APIRouter(prefix="/players", tags=["players"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Register a new player in an event
@router.post("/")
def register_player(name: str, event_id: int, db: Session = Depends(get_db)):
    player = Player(name=name, event_id=event_id)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


# List all players in an event
@router.get("/")
def list_players(event_id: int, db: Session = Depends(get_db)):
    return db.query(Player).filter(Player.event_id == event_id).all()

# List all players (for system stats)
@router.get("/all")
def list_all_players(db: Session = Depends(get_db)):
    return db.query(Player).all()

# Update a player
@router.put("/{player_id}")
def update_player(player_id: int, name: str, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    player.name = name
    db.commit()
    db.refresh(player)
    return player

# Delete a player (hard delete)
@router.delete("/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    db.delete(player)
    db.commit()
    return {"detail": "Player deleted successfully"}
