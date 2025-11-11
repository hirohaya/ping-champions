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

class EventUpdate(BaseModel):
    """Schema for updating event data"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    date: Optional[str] = Field(None, description="Event date in YYYY-MM-DD format")
    time: Optional[str] = Field(None, description="Event time in HH:MM format")
    
    @field_validator('date')
    @classmethod
    def validate_date_format(cls, v):
        """Validate date is in YYYY-MM-DD format"""
        if v is not None and not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v

    @field_validator('time')
    @classmethod
    def validate_time_format(cls, v):
        """Validate time is in HH:MM format"""
        if v is not None and not re.match(r'^\d{2}:\d{2}$', v):
            raise ValueError('Time must be in HH:MM format')
        return v

# ============ Player Schemas ============
class PlayerCreate(BaseModel):
    """Schema for creating a new player"""
    name: str = Field(..., min_length=1, max_length=100, description="Player name")
    event_id: int = Field(..., gt=0, description="Event ID the player is registering for")

class TranslationMessageCreate(BaseModel):
    """Schema for creating a translation message"""
    locale: str = Field(..., min_length=2, max_length=10, description="Locale code (e.g., 'pt-BR')")
    namespace: str = Field(..., min_length=1, max_length=50, description="Namespace (e.g., 'events')")
    key: str = Field(..., min_length=1, max_length=100, description="Translation key")
    value: str = Field(..., min_length=1, description="Translation value")
    note: Optional[str] = Field(None, max_length=500, description="Translator notes")


class TranslationMessageRead(BaseModel):
    """Schema for reading translation data"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    locale: str
    namespace: str
    key: str
    value: str
    version: int
    created_at: datetime
    updated_at: datetime
    note: Optional[str] = None


class LocaleConfigCreate(BaseModel):
    """Schema for creating locale configuration"""
    locale: str = Field(..., min_length=2, max_length=10, description="Locale code")
    name: str = Field(..., min_length=1, max_length=50, description="Display name")
    active: bool = Field(True, description="Whether locale is active")
    default_locale: bool = Field(False, description="Whether this is the default locale")


class LocaleConfigRead(BaseModel):
    """Schema for reading locale configuration"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    locale: str
    name: str
    active: bool
    default_locale: bool
    message_count: int
    created_at: datetime


class PlayerRead(BaseModel):
    """Schema for reading player data"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    event_id: int
    score: int
    ranking: int
    elo_rating: Optional[float] = None
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
    winner_id: Optional[int] = Field(None, gt=0, description="Winning player ID (optional)")
    player1_games: int = Field(0, ge=0, description="Number of games won by player 1")
    player2_games: int = Field(0, ge=0, description="Number of games won by player 2")
    games_score: Optional[str] = Field(None, description="Detailed score per game (e.g., '11-9,10-12,11-8')")
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
    player1_games: int
    player2_games: int
    games_score: Optional[str] = None

class MatchUpdate(BaseModel):
    """Schema for updating match data"""
    winner_id: Optional[int] = Field(None, gt=0, description="Winning player ID")
    player1_games: Optional[int] = Field(None, ge=0, description="Number of games won by player 1")
    player2_games: Optional[int] = Field(None, ge=0, description="Number of games won by player 2")
    games_score: Optional[str] = Field(None, description="Detailed score per game")
    finished: Optional[bool] = Field(None, description="Whether the match is finished")

# ============ Ranking Schemas ============
class RankingEntry(BaseModel):
    """Schema for ranking entry"""
    model_config = ConfigDict(from_attributes=True)
    
    player_id: int
    name: str
    elo: float = Field(default=1600.0, description="ELO rating")
    wins: int = Field(default=0, ge=0)
    losses: int = Field(default=0, ge=0)
    win_rate: float = Field(default=0.0, ge=0.0, le=1.0)

class RankingResponse(BaseModel):
    """Schema for ranking response"""
    model_config = ConfigDict(from_attributes=True)
    
    event_id: int
    entries: list[RankingEntry]
