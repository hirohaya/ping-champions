# Pydantic schemas for request/response validation
import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ============ Event Schemas ============
class EventCreate(BaseModel):
    """Schema for creating a new event"""
    name: str = Field(..., min_length=1, max_length=100, description="Event name")
    date: str = Field(..., description="Event date in YYYY-MM-DD format")
    time: str = Field(..., description="Event time in HH:MM format")

    @field_validator('date')
    @classmethod
    def validate_date_format(cls, v):
        """Validate date is in YYYY-MM-DD format"""
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v

    @field_validator('time')
    @classmethod
    def validate_time_format(cls, v):
        """Validate time is in HH:MM format"""
        if not re.match(r'^\d{2}:\d{2}$', v):
            raise ValueError('Time must be in HH:MM format')
        return v


class EventRead(BaseModel):
    """Schema for reading event data"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    date: str
    time: str
    active: bool
    created_at: Optional[datetime] = None

# ============ Player Schemas ============
class PlayerCreate(BaseModel):
    """Schema for creating a new player"""
    name: str = Field(..., min_length=1, max_length=100, description="Player name")
    event_id: int = Field(..., gt=0, description="Event ID the player is registering for")

class PlayerRead(BaseModel):
    """Schema for reading player data"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    event_id: int
    score: int
    ranking: int
    active: bool

class PlayerUpdate(BaseModel):
    """Schema for updating player data"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    score: Optional[int] = Field(None, ge=0)
    ranking: Optional[int] = Field(None, ge=0)

# ============ Match Schemas ============
class MatchCreate(BaseModel):
    """Schema for creating a new match"""
    event_id: int = Field(..., gt=0, description="Event ID")
    player1_id: int = Field(..., gt=0, description="First player ID")
    player2_id: int = Field(..., gt=0, description="Second player ID")
    best_of: int = Field(default=5, ge=1, le=7, description="Best of N sets (1, 3, 5, or 7)")

    @field_validator('best_of')
    @classmethod
    def validate_best_of(cls, v):
        """Validate best_of is odd number"""
        if v not in [1, 3, 5, 7]:
            raise ValueError('best_of must be 1, 3, 5, or 7')
        return v

class MatchRead(BaseModel):
    """Schema for reading match data"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    event_id: int
    player1_id: int
    player2_id: int
    winner_id: Optional[int] = None
    best_of: int
    finished: bool

class MatchUpdate(BaseModel):
    """Schema for updating match data"""
    winner_id: Optional[int] = Field(None, gt=0)
    finished: Optional[bool] = None

# ============ Ranking Schemas ============
class RankingEntry(BaseModel):
    """Schema for ranking entry"""
    model_config = ConfigDict(from_attributes=True)
    
    player_id: int
    name: str
    wins: int = Field(default=0, ge=0)
    losses: int = Field(default=0, ge=0)
    win_rate: float = Field(default=0.0, ge=0.0, le=1.0)

class RankingResponse(BaseModel):
    """Schema for ranking response"""
    model_config = ConfigDict(from_attributes=True)
    
    event_id: int
    entries: list[RankingEntry]
