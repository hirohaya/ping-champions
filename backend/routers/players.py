# FastAPI imports for API routing and dependency injection
from fastapi import APIRouter, Depends, HTTPException, Query

# SQLAlchemy imports for database session management
from sqlalchemy.orm import Session

from database import SessionLocal

# Import models
from models.event import Event
from models.player import Player

# Import schemas
from schemas import PlayerCreate, PlayerRead, PlayerUpdate

# Router for player-related endpoints
router = APIRouter(prefix="/players", tags=["players"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Register a new player in an event
@router.post("", response_model=PlayerRead, status_code=201)
def register_player(player_data: PlayerCreate, db: Session = Depends(get_db)):
    """
    Register a new player for an event.

    - **name**: Player's name (1-100 characters)
    - **event_id**: Event ID player is registering for
    """
    # Verify event exists
    event = db.query(Event).filter(Event.id == player_data.event_id, Event.active).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    player = Player(name=player_data.name, event_id=player_data.event_id)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


# List all players in an event
@router.get("", response_model=list[PlayerRead])
def list_players(event_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    """
    List all active players in an event.

    - **event_id**: Event ID to filter players
    """
    # Verify event exists
    event = db.query(Event).filter(Event.id == event_id, Event.active).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return db.query(Player).filter(
        Player.event_id == event_id,
        Player.active
    ).all()

# List all players (for system stats)
@router.get("/all", response_model=list[PlayerRead])
def list_all_players(db: Session = Depends(get_db)):
    """List all players in the system (including inactive)"""
    return db.query(Player).all()

# Get a specific player
@router.get("/{player_id}", response_model=PlayerRead)
def get_player(player_id: int, db: Session = Depends(get_db)):
    """Get details of a specific player"""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

# Update a player
@router.put("/{player_id}", response_model=PlayerRead)
def update_player(player_id: int, player_data: PlayerUpdate, db: Session = Depends(get_db)):
    """
    Update player information.

    - **name**: Player's name (optional)
    - **score**: Player's score (optional)
    - **ranking**: Player's ranking (optional)
    """
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    update_data = player_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(player, field, value)

    db.commit()
    db.refresh(player)
    return player

# Delete a player (soft delete)
@router.delete("/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    """Soft delete a player (mark as inactive)"""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    player.active = False
    db.commit()
    return {"detail": "Player marked as inactive"}
