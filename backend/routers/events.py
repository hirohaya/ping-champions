
# FastAPI imports for API routing and dependency injection
from fastapi import APIRouter, Depends, HTTPException
# SQLAlchemy imports for database session management
from sqlalchemy.orm import Session
from database import SessionLocal
# Import Event model
from models.event import Event
# Utilities
from datetime import datetime
# Pydantic for request validation
from pydantic import BaseModel


# Pydantic schema for event creation requests
class EventCreate(BaseModel):
    name: str  # Event name
    date: str  # Event date in YYYY-MM-DD format
    time: str  # Event time (HH:MM)

router = APIRouter(prefix="/events", tags=["events"])

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# List all active events
@router.get("/")
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).filter(Event.active == True).all()


# Create a new event
@router.post("/create")
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    try:
        # Parse date string to datetime object
        date_dt = datetime.strptime(event.date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    new_event = Event(name=event.name, date=date_dt, time=event.time)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


# Soft delete an event (mark as inactive)
@router.post("/delete/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event.active = False  # Soft delete
    db.commit()
    return {"detail": "Event marked as inactive (soft deleted) successfully"}
