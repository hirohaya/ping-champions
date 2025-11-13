# Pydantic schemas for request/response validation
import re
from datetime import datetime
from typing import Optional
from enum import Enum

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
    winner_id: Optional[int] = Field(None, gt=0, description="Winning player ID (can be set later)")
    player1_games: Optional[int] = Field(None, ge=0, description="Number of games won by player 1 (can be set later)")
    player2_games: Optional[int] = Field(None, ge=0, description="Number of games won by player 2 (can be set later)")
    games_score: Optional[str] = Field(None, description="Detailed score per game (can be set later)")
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
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
    
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


class MatchResultResponse(BaseModel):
    """Schema for match result with ELO calculations"""
    match_id: int
    winner_id: int
    player1_id: int
    player2_id: int
    player1_rating_before: float
    player1_rating_after: float
    player1_rating_change: float
    player2_rating_before: float
    player2_rating_after: float
    player2_rating_change: float
    player1_k_factor: int = Field(description="K-factor used for player 1")
    player2_k_factor: int = Field(description="K-factor used for player 2")

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


# ============ Membership Schemas ============
class MembershipStatusEnum(str, Enum):
    """Membership status options"""
    CONVIDADO = "convidado"
    ATIVO = "ativo"
    INATIVO = "inativo"
    SUSPENSO = "suspenso"
    DELETADO = "deletado"


class MembershipCreate(BaseModel):
    """Schema for creating a membership (inviting a player)"""
    event_id: int = Field(..., gt=0, description="Event ID")
    player_id: int = Field(..., gt=0, description="Player ID to invite")


class MembershipRead(BaseModel):
    """Schema for reading membership data"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    event_id: int
    player_id: int
    status: MembershipStatusEnum
    data_entrada: Optional[datetime] = Field(None, description="Date when player joined")
    data_saida: Optional[datetime] = Field(None, description="Date when player left")
    data_suspensao: Optional[datetime] = Field(None, description="Date when player was suspended")
    motivo_suspensao: Optional[str] = Field(None, description="Reason for suspension")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class MembershipUpdate(BaseModel):
    """Schema for updating membership status"""
    status: Optional[MembershipStatusEnum] = None
    motivo_suspensao: Optional[str] = Field(None, max_length=255, description="Reason for suspension")


class MembershipAcceptInvite(BaseModel):
    """Schema for accepting membership invite"""
    pass  # No fields needed, just acceptance


class MembershipLeave(BaseModel):
    """Schema for leaving a group"""
    pass  # No fields needed, just confirmation


class MembershipSuspend(BaseModel):
    """Schema for suspending a member"""
    motivo_suspensao: Optional[str] = Field(None, max_length=255, description="Reason for suspension")


class MembershipReactivate(BaseModel):
    """Schema for reactivating a suspended member"""
    pass  # No fields needed, just confirmation


# ============ Tournament Schemas ============
class TournamentTypeEnum(str, Enum):
    """Tournament type options"""
    SINGLE_ELIMINATION = "SINGLE_ELIMINATION"
    SWISS = "SWISS"
    GROUP_KNOCKOUT = "GROUP_KNOCKOUT"
    ROUND_ROBIN = "ROUND_ROBIN"


class TournamentStatusEnum(str, Enum):
    """Tournament status options"""
    CREATED = "CREATED"
    STARTING = "STARTING"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"


class TournamentCreate(BaseModel):
    """Schema for creating a tournament"""
    event_id: int = Field(..., gt=0, description="Event ID")
    name: str = Field(..., min_length=1, max_length=255, description="Tournament name")
    tournament_type: TournamentTypeEnum = Field(..., description="Type of tournament")
    max_participants: Optional[int] = Field(None, gt=1, description="Maximum participants (None = unlimited)")
    best_of: int = Field(default=1, ge=1, le=7, description="For SINGLE_ELIMINATION: 1, 3, 5, or 7")
    num_groups: int = Field(default=2, ge=2, le=16, description="For GROUP_KNOCKOUT: number of groups")
    swiss_rounds: int = Field(default=3, ge=1, le=10, description="For SWISS: number of rounds")
    allow_draws: bool = Field(default=False, description="For ROUND_ROBIN: allow draws")

    @field_validator('best_of')
    @classmethod
    def validate_best_of(cls, v):
        """Validate best_of for SINGLE_ELIMINATION"""
        if v not in [1, 3, 5, 7]:
            raise ValueError('best_of must be 1, 3, 5, or 7')
        return v


class TournamentRead(BaseModel):
    """Schema for reading tournament data"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    event_id: int
    name: str
    tournament_type: TournamentTypeEnum
    status: TournamentStatusEnum
    current_round: int
    participant_count: int
    max_participants: Optional[int] = None
    best_of: int
    num_groups: int
    swiss_rounds: int
    allow_draws: bool
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    participants_ids: list[int] = Field(default_factory=list)
    bracket: Optional[dict] = Field(default=None, description="Tournament bracket structure")


class TournamentUpdate(BaseModel):
    """Schema for updating tournament"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    max_participants: Optional[int] = Field(None, gt=1)


class TournamentAddParticipant(BaseModel):
    """Schema for adding a participant to tournament"""
    player_id: int = Field(..., gt=0, description="Player ID to add")


class TournamentRemoveParticipant(BaseModel):
    """Schema for removing a participant from tournament"""
    player_id: int = Field(..., gt=0, description="Player ID to remove")


class TournamentStart(BaseModel):
    """Schema for starting a tournament"""
    pass  # No fields needed, just confirmation


class TournamentAdvanceRound(BaseModel):
    """Schema for advancing to next round"""
    pass  # No fields needed, just confirmation


class TournamentFinish(BaseModel):
    """Schema for finishing a tournament"""
    pass  # No fields needed, just confirmation


class TournamentCancel(BaseModel):
    """Schema for cancelling a tournament"""
    pass  # No fields needed, just confirmation