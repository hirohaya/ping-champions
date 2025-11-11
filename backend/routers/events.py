
# FastAPI imports for API routing and dependency injection
from fastapi import APIRouter, Depends, HTTPException

# SQLAlchemy imports for database session management
from sqlalchemy.orm import Session

from database import SessionLocal

# Import Event model
from models.event import Event

# Import schemas
from schemas import EventCreate, EventRead, EventUpdate

router = APIRouter(prefix="/events", tags=["events"])

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# List all events (active and inactive)
@router.get("", response_model=list[EventRead])
def list_events(db: Session = Depends(get_db)):
    """
    List all events (active and inactive).

    Returns a list of all events, sorted by active status (active first) and then by date.
    """
    return db.query(Event).order_by(Event.active.desc(), Event.date.desc()).all()


# Get a specific event
@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific event.
    
    Works for both active and inactive events.

    - **event_id**: The event ID to retrieve
    """
    event = db.query(Event).filter(Event.id == event_id).first()
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
    new_event = Event(name=event.name, date=event.date, time=event.time)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


# Update event information
@router.put("/{event_id}", response_model=EventRead)
def update_event(event_id: int, event_data: EventUpdate, db: Session = Depends(get_db)):
    """
    Update event information.

    - **name**: Event name (optional)
    - **date**: Event date in YYYY-MM-DD format (optional)
    - **time**: Event time in HH:MM format (optional)
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    update_data = event_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)

    db.commit()
    db.refresh(event)
    return event


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
