"""
Tournament Management Router

Handles CRUD operations for tournaments and tournament-related functionality.
Supports 4 tournament types: Single Elimination, Swiss, Group+Knockout, Round Robin.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import SessionLocal
from models import Tournament, Event, Player, Match, TournamentStatus
from schemas import (
    TournamentCreate, TournamentRead, TournamentUpdate,
    TournamentAddParticipant, TournamentRemoveParticipant,
    TournamentStart, TournamentAdvanceRound, TournamentFinish,
    TournamentCancel
)

router = APIRouter(
    prefix="/tournaments",
    tags=["tournaments"],
    responses={404: {"description": "Tournament not found"}}
)


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============ Helper Functions ============

def get_tournament_or_404(tournament_id: int, db: Session) -> Tournament:
    """Get tournament or raise 404 error"""
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament


def get_event_or_404(event_id: int, db: Session) -> Event:
    """Get event or raise 404 error"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


def get_player_or_404(player_id: int, db: Session) -> Player:
    """Get player or raise 404 error"""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


# ============ List & Create Endpoints ============

@router.get("/", response_model=List[TournamentRead])
def list_tournaments(
    event_id: Optional[int] = Query(None, description="Filter by event ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """
    List all tournaments with optional filters
    
    Query Parameters:
    - event_id: Filter by event (optional)
    - status: Filter by status (CREATED, STARTING, IN_PROGRESS, FINISHED, CANCELLED)
    """
    query = db.query(Tournament)
    
    if event_id:
        query = query.filter(Tournament.event_id == event_id)
    
    if status:
        query = query.filter(Tournament.status == status)
    
    tournaments = query.all()
    return tournaments


@router.post("/", response_model=TournamentRead)
def create_tournament(
    tournament_data: TournamentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new tournament
    
    Tournament types:
    - SINGLE_ELIMINATION: Single elimination bracket (best_of: 1, 3, 5, or 7)
    - SWISS: Swiss system with multiple rounds (swiss_rounds: 1-10)
    - GROUP_KNOCKOUT: Groups stage then knockout (num_groups: 2-16)
    - ROUND_ROBIN: All teams play all teams (allow_draws: True/False)
    """
    # Verify event exists
    event = get_event_or_404(tournament_data.event_id, db)
    
    # Create tournament
    tournament = Tournament(
        event_id=tournament_data.event_id,
        name=tournament_data.name,
        tournament_type=tournament_data.tournament_type,
        max_participants=tournament_data.max_participants,
        best_of=tournament_data.best_of,
        num_groups=tournament_data.num_groups,
        swiss_rounds=tournament_data.swiss_rounds,
        allow_draws=tournament_data.allow_draws,
        status="CREATED",
        created_at=datetime.now(),
        participants_ids=[]
    )
    
    db.add(tournament)
    db.commit()
    db.refresh(tournament)
    
    return tournament


# ============ Detail Endpoints ============

@router.get("/{tournament_id}", response_model=TournamentRead)
def get_tournament(
    tournament_id: int,
    db: Session = Depends(get_db)
):
    """Get tournament details"""
    tournament = get_tournament_or_404(tournament_id, db)
    return tournament


@router.put("/{tournament_id}", response_model=TournamentRead)
def update_tournament(
    tournament_id: int,
    tournament_data: TournamentUpdate,
    db: Session = Depends(get_db)
):
    """Update tournament settings"""
    tournament = get_tournament_or_404(tournament_id, db)
    
    # Check if tournament can be updated (only in CREATED status)
    if tournament.status != TournamentStatus.CREATED:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot update tournament in {tournament.status} status"
        )
    
    # Update fields
    if tournament_data.name:
        tournament.name = tournament_data.name
    if tournament_data.max_participants is not None:
        tournament.max_participants = tournament_data.max_participants
    
    db.commit()
    db.refresh(tournament)
    
    return tournament


# ============ Participant Management ============

@router.post("/{tournament_id}/participants", response_model=TournamentRead)
def add_participant(
    tournament_id: int,
    participant_data: TournamentAddParticipant,
    db: Session = Depends(get_db)
):
    """
    Add a participant to tournament
    
    - Player must exist in the event
    - Player must not already be in tournament
    - Tournament must be in CREATED status
    - Cannot exceed max_participants limit
    """
    tournament = get_tournament_or_404(tournament_id, db)
    player = get_player_or_404(participant_data.player_id, db)
    
    # Verify player is in the event
    if player.event_id != tournament.event_id:
        raise HTTPException(
            status_code=400,
            detail="Player is not in this event"
        )
    
    # Check if tournament can accept participants
    if tournament.status != TournamentStatus.CREATED:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot add participants to tournament in {tournament.status} status"
        )
    
    # Check if player already in tournament
    if tournament.has_participant(participant_data.player_id):
        raise HTTPException(
            status_code=400,
            detail="Player already in tournament"
        )
    
    # Check max participants limit
    if tournament.max_participants and tournament.participant_count >= tournament.max_participants:
        raise HTTPException(
            status_code=400,
            detail=f"Tournament is full (max: {tournament.max_participants})"
        )
    
    # Add participant
    tournament.add_participant(participant_data.player_id)
    from sqlalchemy.orm import attributes
    attributes.flag_modified(tournament, "participants_ids")
    db.commit()
    db.refresh(tournament)
    
    return tournament


@router.delete("/{tournament_id}/participants/{player_id}", response_model=TournamentRead)
def remove_participant(
    tournament_id: int,
    player_id: int,
    db: Session = Depends(get_db)
):
    """
    Remove a participant from tournament
    
    - Player must be in tournament
    - Tournament must be in CREATED status (cannot remove after started)
    """
    tournament = get_tournament_or_404(tournament_id, db)
    
    # Check if tournament can remove participants
    if tournament.status != TournamentStatus.CREATED:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot remove participants from tournament in {tournament.status} status"
        )
    
    # Check if player in tournament
    if not tournament.has_participant(player_id):
        raise HTTPException(
            status_code=400,
            detail="Player is not in this tournament"
        )
    
    # Remove participant
    tournament.remove_participant(player_id)
    from sqlalchemy.orm import attributes
    attributes.flag_modified(tournament, "participants_ids")
    db.commit()
    db.refresh(tournament)
    
    return tournament


# ============ Tournament State Transitions ============

@router.post("/{tournament_id}/start", response_model=TournamentRead)
def start_tournament(
    tournament_id: int,
    start_data: TournamentStart,
    db: Session = Depends(get_db)
):
    """
    Start a tournament
    
    - Tournament must be in CREATED status
    - Must have at least 2 participants
    - Generates initial bracket based on tournament type
    """
    tournament = get_tournament_or_404(tournament_id, db)
    
    # Check status
    if tournament.status != TournamentStatus.CREATED:
        raise HTTPException(
            status_code=400,
            detail=f"Tournament is already {tournament.status}"
        )
    
    # Check minimum participants
    if tournament.participant_count < 2:
        raise HTTPException(
            status_code=400,
            detail=f"Need at least 2 participants (have {tournament.participant_count})"
        )
    
    # Generate initial bracket
    from utils.bracket_generator import BracketGenerator
    bracket_gen = BracketGenerator()
    
    try:
        # Start tournament (moves to STARTING status)
        tournament.start()
        
        # Generate bracket
        bracket = bracket_gen.generate(
            tournament_type=tournament.tournament_type,
            participants_ids=tournament.participants_ids,
            best_of=tournament.best_of,
            num_groups=tournament.num_groups,
            swiss_rounds=tournament.swiss_rounds
        )
        tournament.bracket = bracket
        from sqlalchemy.orm import attributes
        attributes.flag_modified(tournament, "bracket")
        
        # Transition to IN_PROGRESS
        tournament.status = TournamentStatus.IN_PROGRESS
        
        db.commit()
        db.refresh(tournament)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Failed to start tournament: {str(e)}"
        )
    
    return tournament


@router.post("/{tournament_id}/advance-round", response_model=TournamentRead)
def advance_round(
    tournament_id: int,
    advance_data: TournamentAdvanceRound,
    db: Session = Depends(get_db)
):
    """
    Advance tournament to next round
    
    - Tournament must be IN_PROGRESS
    - All matches in current round must be completed
    """
    tournament = get_tournament_or_404(tournament_id, db)
    
    # Check status
    if tournament.status != TournamentStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=400,
            detail=f"Tournament must be IN_PROGRESS (current: {tournament.status})"
        )
    
    # Check all current round matches are completed
    incomplete_matches = db.query(Match).filter(
        Match.tournament_id == tournament_id,
        Match.round == tournament.current_round,
        Match.winner_id == None
    ).count()
    
    if incomplete_matches > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot advance: {incomplete_matches} matches still incomplete in round {tournament.current_round}"
        )
    
    # Advance round
    tournament.advance_round()
    db.commit()
    db.refresh(tournament)
    
    return tournament


@router.post("/{tournament_id}/finish", response_model=TournamentRead)
def finish_tournament(
    tournament_id: int,
    finish_data: TournamentFinish,
    db: Session = Depends(get_db)
):
    """
    Finish a tournament
    
    - Tournament must be IN_PROGRESS
    - All final matches must be completed
    """
    tournament = get_tournament_or_404(tournament_id, db)
    
    # Check status
    if tournament.status != TournamentStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=400,
            detail=f"Tournament must be IN_PROGRESS (current: {tournament.status})"
        )
    
    # Check if final match is completed
    final_matches = db.query(Match).filter(
        Match.tournament_id == tournament_id,
        Match.round == tournament.current_round,
        Match.winner_id == None
    ).count()
    
    if final_matches > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot finish: {final_matches} final match(es) still incomplete"
        )
    
    # Finish tournament
    tournament.finish()
    tournament.finished_at = datetime.now()
    tournament.status = "FINISHED"
    
    db.commit()
    db.refresh(tournament)
    
    return tournament


@router.post("/{tournament_id}/cancel", response_model=TournamentRead)
def cancel_tournament(
    tournament_id: int,
    cancel_data: TournamentCancel,
    db: Session = Depends(get_db)
):
    """
    Cancel a tournament
    
    - Can only cancel in CREATED or IN_PROGRESS status
    """
    tournament = get_tournament_or_404(tournament_id, db)
    
    # Check status
    if tournament.status in ["FINISHED", "CANCELLED"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel tournament in {tournament.status} status"
        )
    
    # Cancel tournament
    tournament.cancel()
    tournament.status = "CANCELLED"
    
    db.commit()
    db.refresh(tournament)
    
    return tournament


# ============ Bracket & Matches Endpoints ============

@router.get("/{tournament_id}/bracket")
def get_bracket(
    tournament_id: int,
    round_num: Optional[int] = Query(None, description="Get specific round (optional)"),
    db: Session = Depends(get_db)
):
    """
    Get tournament bracket structure
    
    Query Parameters:
    - round_num: Get specific round details (optional)
    """
    tournament = get_tournament_or_404(tournament_id, db)
    
    if not tournament.bracket:
        raise HTTPException(
            status_code=400,
            detail="Tournament bracket not yet generated"
        )
    
    if round_num and round_num > tournament.current_round:
        raise HTTPException(
            status_code=400,
            detail=f"Round {round_num} not yet available (current: {tournament.current_round})"
        )
    
    return {
        "tournament_id": tournament_id,
        "tournament_type": tournament.tournament_type,
        "current_round": tournament.current_round,
        "bracket": tournament.bracket
    }


@router.get("/{tournament_id}/matches")
def get_tournament_matches(
    tournament_id: int,
    round_num: Optional[int] = Query(None, description="Filter by round"),
    db: Session = Depends(get_db)
):
    """
    Get all matches in tournament with optional round filter
    
    Query Parameters:
    - round_num: Filter by specific round (optional)
    """
    tournament = get_tournament_or_404(tournament_id, db)
    
    query = db.query(Match).filter(Match.tournament_id == tournament_id)
    
    if round_num:
        query = query.filter(Match.round == round_num)
    
    matches = query.all()
    
    return {
        "tournament_id": tournament_id,
        "total_matches": len(matches),
        "matches": matches
    }


@router.get("/{tournament_id}/standings")
def get_tournament_standings(
    tournament_id: int,
    db: Session = Depends(get_db)
):
    """
    Get tournament standings/rankings
    
    Returns current standings based on match results.
    Format depends on tournament type.
    """
    tournament = get_tournament_or_404(tournament_id, db)
    
    # Get all matches in tournament
    matches = db.query(Match).filter(Match.tournament_id == tournament_id).all()
    
    # Calculate standings based on results
    standings = {}
    for player_id in tournament.participants_ids:
        standings[player_id] = {
            "player_id": player_id,
            "wins": 0,
            "losses": 0,
            "draws": 0
        }
    
    for match in matches:
        if match.winner_id:
            standings[match.winner_id]["wins"] += 1
            standings[match.loser_id]["losses"] += 1
        elif match.winner_id is None and tournament.allow_draws:
            standings[match.p1_id]["draws"] += 1
            standings[match.p2_id]["draws"] += 1
    
    # Sort by wins, then draws
    sorted_standings = sorted(
        standings.values(),
        key=lambda x: (x["wins"], x["draws"]),
        reverse=True
    )
    
    return {
        "tournament_id": tournament_id,
        "tournament_type": tournament.tournament_type,
        "status": tournament.status,
        "current_round": tournament.current_round,
        "standings": sorted_standings
    }
