# Pydantic schemas for request/response validation
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ============ Event Schemas ============
class EventCreate(BaseModel):
    name: str
    date: str  # YYYY-MM-DD format
    time: str  # HH:MM format

class EventRead(BaseModel):
    id: int
    name: str
    date: datetime
    time: str
    active: bool
    
    class Config:
        from_attributes = True

# ============ Player Schemas ============
class PlayerCreate(BaseModel):
    name: str
    event_id: int

class PlayerRead(BaseModel):
    id: int
    name: str
    event_id: int
    score: int
    ranking: int
    active: int
    
    class Config:
        from_attributes = True

class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    score: Optional[int] = None
    ranking: Optional[int] = None

# ============ Match Schemas ============
class MatchCreate(BaseModel):
    event_id: int
    player1_id: int
    player2_id: int
    best_of: Optional[int] = 5

class MatchRead(BaseModel):
    id: int
    event_id: int
    player1_id: int
    player2_id: int
    winner_id: Optional[int] = None
    best_of: int
    finished: int
    
    class Config:
        from_attributes = True

class MatchUpdate(BaseModel):
    winner_id: Optional[int] = None
    finished: Optional[int] = None

# ============ Ranking Schemas ============
class RankingEntry(BaseModel):
    player_id: int
    name: str
    wins: int
    losses: int
    win_rate: float
    
    class Config:
        from_attributes = True
