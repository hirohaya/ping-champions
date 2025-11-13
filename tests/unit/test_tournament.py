"""Unit tests for Tournament model and Bracket Generator"""

import pytest
from datetime import datetime
import sys
import os
from sqlalchemy.orm import attributes

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from models import Tournament, Event, Player, TournamentType, TournamentStatus
from utils.bracket_generator import BracketGenerator


class TestTournamentModel:
    """Test Tournament model functionality"""
    
    @pytest.fixture
    def event(self, db_session):
        """Create a test event"""
        event = Event(
            name="Test Event",
            date="2025-01-15",
            time="18:00",
            active=True
        )
        db_session.add(event)
        db_session.commit()
        return event
    
    @pytest.fixture
    def players(self, db_session, event):
        """Create test players"""
        players = []
        for i in range(1, 5):
            player = Player(
                name=f"Player {i}",
                event_id=event.id,
                elo_rating=1600
            )
            db_session.add(player)
            players.append(player)
        db_session.commit()
        return players
    
    @pytest.fixture
    def tournament(self, db_session, event):
        """Create an empty test tournament (no participants)"""
        tournament = Tournament(
            event_id=event.id,
            name="Test Tournament",
            tournament_type=TournamentType.SINGLE_ELIMINATION,
            status=TournamentStatus.CREATED,
            best_of=1,
            num_groups=2,
            swiss_rounds=3,
            allow_draws=False,
            created_at=datetime.now(),
            participants_ids=[]
        )
        db_session.add(tournament)
        db_session.commit()
        return tournament
    
    @pytest.fixture
    def tournament_with_participants(self, db_session, event, players):
        """Create a test tournament with 2 participants"""
        tournament = Tournament(
            event_id=event.id,
            name="Test Tournament",
            tournament_type=TournamentType.SINGLE_ELIMINATION,
            status=TournamentStatus.CREATED,
            best_of=1,
            num_groups=2,
            swiss_rounds=3,
            allow_draws=False,
            created_at=datetime.now(),
            participants_ids=[]
        )
        db_session.add(tournament)
        db_session.commit()
        
        # Add first 2 players to tournament
        tournament.add_participant(players[0].id)
        tournament.add_participant(players[1].id)
        attributes.flag_modified(tournament, "participants_ids")
        db_session.commit()
        return tournament
    
    def test_tournament_creation(self, tournament):
        """Test tournament can be created"""
        assert tournament.id is not None
        assert tournament.name == "Test Tournament"
        assert tournament.status == TournamentStatus.CREATED
        assert tournament.participant_count == 0
    
    def test_add_participant(self, tournament, players, db_session):
        """Test adding a participant"""
        tournament.add_participant(players[0].id)
        # Flag participants_ids as modified (JSON field)
        attributes.flag_modified(tournament, "participants_ids")
        db_session.commit()
        
        assert tournament.participant_count == 1
        assert tournament.has_participant(players[0].id)
        assert tournament.participants_ids == [players[0].id]
    
    def test_add_multiple_participants(self, tournament, players, db_session):
        """Test adding multiple participants"""
        for player in players:
            tournament.add_participant(player.id)
        # Flag participants_ids as modified (JSON field)
        attributes.flag_modified(tournament, "participants_ids")
        db_session.commit()
        
        assert tournament.participant_count == 4
        for player in players:
            assert tournament.has_participant(player.id)
    
    def test_remove_participant(self, tournament, players, db_session):
        """Test removing a participant"""
        tournament.add_participant(players[0].id)
        tournament.add_participant(players[1].id)
        attributes.flag_modified(tournament, "participants_ids")
        db_session.commit()
        
        tournament.remove_participant(players[0].id)
        attributes.flag_modified(tournament, "participants_ids")
        db_session.commit()
        
        assert tournament.participant_count == 1
        assert not tournament.has_participant(players[0].id)
        assert tournament.has_participant(players[1].id)
    
    def test_is_full(self, tournament, players, db_session):
        """Test tournament full detection"""
        tournament.max_participants = 2
        tournament.add_participant(players[0].id)
        tournament.add_participant(players[1].id)
        attributes.flag_modified(tournament, "participants_ids")
        db_session.commit()
        
        assert tournament.is_full
    
    def test_can_start(self, tournament, players, db_session):
        """Test tournament can start validation"""
        # Can't start with 0 participants
        assert not tournament.can_start
        
        # Can't start with 1 participant
        tournament.add_participant(players[0].id)
        attributes.flag_modified(tournament, "participants_ids")
        db_session.commit()
        assert not tournament.can_start
        
        # Can start with 2+ participants
        tournament.add_participant(players[1].id)
        attributes.flag_modified(tournament, "participants_ids")
        db_session.commit()
        assert tournament.can_start
    
    def test_tournament_status_transitions(self, tournament_with_participants, db_session):
        """Test tournament status state machine"""
        tournament = tournament_with_participants
        assert tournament.status == TournamentStatus.CREATED
        
        # Start
        result = tournament.start()
        assert result is True  # start() should return True on success
        assert tournament.status == TournamentStatus.STARTING  # Method sets status to STARTING
        assert tournament.started_at is not None
        assert tournament.current_round == 1
        db_session.commit()
        
        # Transition to IN_PROGRESS (simulating router action)
        tournament.status = TournamentStatus.IN_PROGRESS
        db_session.flush()  # Flush changes to database session
        db_session.commit()
        
        # Verify status was updated
        assert tournament.status == TournamentStatus.IN_PROGRESS
        
        # Advance round
        result = tournament.advance_round()
        assert result is True
        assert tournament.current_round == 2
        db_session.commit()
        
        # Finish
        result = tournament.finish()
        assert result is True
        assert tournament.status == TournamentStatus.FINISHED
        assert tournament.finished_at is not None
        db_session.commit()
    
    def test_cancel_tournament(self, tournament, db_session):
        """Test cancelling a tournament"""
        tournament.cancel()
        
        assert tournament.status == TournamentStatus.CANCELLED


class TestBracketGenerator:
    """Test bracket generation for different tournament types"""
    
    @pytest.fixture
    def generator(self):
        """Create bracket generator"""
        return BracketGenerator()
    
    @pytest.fixture
    def players_ids(self):
        """Generate list of player IDs"""
        return list(range(1, 9))  # Players 1-8
    
    def test_single_elimination_bracket(self, generator, players_ids):
        """Test single elimination bracket generation"""
        bracket = generator.generate(
            tournament_type="SINGLE_ELIMINATION",
            participants_ids=players_ids,
            best_of=1
        )
        
        assert bracket["type"] == "SINGLE_ELIMINATION"
        assert bracket["total_rounds"] == 3  # 8 players = 3 rounds
        assert len(bracket["rounds"][1]) == 4  # First round: 4 matches
        assert len(bracket["rounds"][2]) == 2  # Second round: 2 matches
        assert len(bracket["rounds"][3]) == 1  # Third round: 1 match (final)
    
    def test_single_elimination_odd_players(self, generator):
        """Test single elimination with odd number of players"""
        players = list(range(1, 6))  # 5 players
        bracket = generator.generate(
            tournament_type="SINGLE_ELIMINATION",
            participants_ids=players
        )
        
        assert bracket["type"] == "SINGLE_ELIMINATION"
        assert bracket["total_rounds"] == 3  # 5 players = 3 rounds (8 slots)
    
    def test_swiss_bracket(self, generator, players_ids):
        """Test Swiss system bracket generation"""
        bracket = generator.generate(
            tournament_type="SWISS",
            participants_ids=players_ids,
            swiss_rounds=3
        )
        
        assert bracket["type"] == "SWISS"
        assert bracket["total_rounds"] == 3
        assert len(bracket["rounds"]) == 3
        
        # Check first round pairings
        first_round = bracket["rounds"][1]
        assert len(first_round) == 4  # 8 players = 4 matches
        
        # All players should be paired
        all_players_in_round = set()
        for match in first_round:
            if match["p1_id"]:
                all_players_in_round.add(match["p1_id"])
            if match["p2_id"]:
                all_players_in_round.add(match["p2_id"])
        
        assert len(all_players_in_round) == 8
    
    def test_swiss_odd_players(self, generator):
        """Test Swiss with odd number of players (should have bye)"""
        players = list(range(1, 6))  # 5 players
        bracket = generator.generate(
            tournament_type="SWISS",
            participants_ids=players,
            swiss_rounds=3
        )
        
        first_round = bracket["rounds"][1]
        
        # Should have 2 matches + 1 bye
        assert len(first_round) == 3
        
        # One match should be a bye (p2_id is None)
        bye_count = sum(1 for match in first_round if match["p2_id"] is None)
        assert bye_count == 1
    
    def test_group_knockout_bracket(self, generator, players_ids):
        """Test group + knockout bracket generation"""
        bracket = generator.generate(
            tournament_type="GROUP_KNOCKOUT",
            participants_ids=players_ids,
            num_groups=2
        )
        
        assert bracket["type"] == "GROUP_KNOCKOUT"
        assert bracket["num_groups"] == 2
        
        # Check groups exist
        group_stage = bracket["phases"]["group_stage"]
        assert len(group_stage["groups"]) == 2
        
        # Check each group has 4 players
        for group_players in group_stage["groups"].values():
            assert len(group_players) == 4
        
        # Check knockout stage exists
        knockout_stage = bracket["phases"]["knockout_stage"]
        assert len(knockout_stage["rounds"]) > 0
    
    def test_group_knockout_multiple_groups(self, generator):
        """Test group knockout with different number of groups"""
        players = list(range(1, 17))  # 16 players
        bracket = generator.generate(
            tournament_type="GROUP_KNOCKOUT",
            participants_ids=players,
            num_groups=4
        )
        
        assert bracket["num_groups"] == 4
        group_stage = bracket["phases"]["group_stage"]
        assert len(group_stage["groups"]) == 4
        
        # Each group should have 4 players
        for group_players in group_stage["groups"].values():
            assert len(group_players) == 4
    
    def test_round_robin_bracket(self, generator, players_ids):
        """Test round robin bracket generation"""
        bracket = generator.generate(
            tournament_type="ROUND_ROBIN",
            participants_ids=players_ids
        )
        
        assert bracket["type"] == "ROUND_ROBIN"
        assert bracket["total_players"] == 8
        assert bracket["total_matches"] == 28  # 8 * 7 / 2 = 28
        
        # Check all matches
        matches = bracket["rounds"][1]
        assert len(matches) == 28
    
    def test_match_count_calculation(self, generator):
        """Test match count calculations for each type"""
        n_players = 8
        
        # Single elimination: n-1
        se_matches = generator.calculate_match_count(
            n_players, "SINGLE_ELIMINATION"
        )
        assert se_matches == 7
        
        # Round robin: n(n-1)/2
        rr_matches = generator.calculate_match_count(
            n_players, "ROUND_ROBIN"
        )
        assert rr_matches == 28
        
        # Swiss: approximate
        swiss_matches = generator.calculate_match_count(
            n_players, "SWISS"
        )
        assert swiss_matches > 0
    
    def test_bracket_generator_errors(self, generator):
        """Test bracket generator error handling"""
        # Too few players for single elimination
        with pytest.raises(ValueError):
            generator.generate(
                tournament_type="SINGLE_ELIMINATION",
                participants_ids=[1]
            )
        
        # Unknown tournament type
        with pytest.raises(ValueError):
            generator.generate(
                tournament_type="UNKNOWN_TYPE",
                participants_ids=list(range(1, 9))
            )
        
        # Too few players for group knockout
        with pytest.raises(ValueError):
            generator.generate(
                tournament_type="GROUP_KNOCKOUT",
                participants_ids=list(range(1, 3)),  # Only 2 players
                num_groups=4
            )
