
# FastAPI imports for API routing and dependency injection
# Utilities
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

# SQLAlchemy imports for database session management
from sqlalchemy.orm import Session

from database import SessionLocal

# Import Event model
from models.event import Event

# Import schemas
from schemas import EventCreate, EventRead

router = APIRouter(prefix="/events", tags=["events"])

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# List all active events
@router.get("", response_model=list[EventRead])
def list_events(db: Session = Depends(get_db)):
    """
    List all active events.

    Returns a list of all non-deleted events.
    """
    return db.query(Event).filter(Event.active).all()


# Get a specific event
@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific event.

    - **event_id**: The event ID to retrieve
    """
    event = db.query(Event).filter(Event.id == event_id, Event.active).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


# Create a new event
@router.post("", response_model=EventRead, status_code=201)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """
    Create a new event.

    - **name**: Event name (1-100 characters)
    - **date**: Event date in YYYY-MM-DD format
    - **time**: Event time in HH:MM format
    """
    try:
        # Validate date format
        datetime.strptime(event.date, "%Y-%m-%d")
    except ValueError as err:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD") from err

    new_event = Event(name=event.name, date=event.date, time=event.time)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


# Soft delete an event (mark as inactive)
@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """
    Soft delete an event (mark as inactive).

    - **event_id**: The event ID to delete
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event.active = False  # Soft delete
    db.commit()
    return {"detail": "Event marked as inactive"}
