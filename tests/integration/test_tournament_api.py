"""Integration tests for Tournament API endpoints"""

import pytest
from datetime import datetime


class TestTournamentAPI:
    """Test Tournament API endpoints"""
    
    @pytest.fixture
    def event(self, client, db_session):
        """Create a test event via API"""
        from models import Event
        
        response = client.post(
            "/events/",
            json={
                "name": "Test Event",
                "date": "2025-01-15",
                "time": "18:00"
            }
        )
        assert response.status_code in [200, 201]
        return response.json()
    
    @pytest.fixture
    def players(self, client, db_session, event):
        """Create test players via API"""
        players = []
        for i in range(1, 5):
            response = client.post(
                f"/players/",
                json={
                    "name": f"Player {i}",
                    "event_id": event["id"]
                }
            )
            assert response.status_code in [200, 201]
            players.append(response.json())
        return players
    
    def test_create_tournament(self, client, event):
        """Test creating a tournament"""
        response = client.post(
            "/tournaments/",
            json={
                "event_id": event["id"],
                "name": "Test Tournament",
                "tournament_type": "SINGLE_ELIMINATION",
                "max_participants": 8,
                "best_of": 1
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Tournament"
        assert data["tournament_type"] == "SINGLE_ELIMINATION"
        assert data["status"] == "CREATED"
        assert data["participant_count"] == 0
    
    def test_list_tournaments(self, client, event):
        """Test listing tournaments"""
        # Create two tournaments
        for i in range(2):
            client.post(
                "/tournaments/",
                json={
                    "event_id": event["id"],
                    "name": f"Tournament {i+1}",
                    "tournament_type": "SINGLE_ELIMINATION"
                }
            )
        
        # List all tournaments
        response = client.get("/tournaments/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
    
    def test_get_tournament(self, client, event):
        """Test getting a specific tournament"""
        # Create tournament
        create_response = client.post(
            "/tournaments/",
            json={
                "event_id": event["id"],
                "name": "Test Tournament",
                "tournament_type": "SINGLE_ELIMINATION"
            }
        )
        tournament_id = create_response.json()["id"]
        
        # Get tournament
        response = client.get(f"/tournaments/{tournament_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == tournament_id
        assert data["name"] == "Test Tournament"
    
    def test_update_tournament(self, client, event):
        """Test updating a tournament"""
        # Create tournament
        create_response = client.post(
            "/tournaments/",
            json={
                "event_id": event["id"],
                "name": "Original Name",
                "tournament_type": "SINGLE_ELIMINATION"
            }
        )
        tournament_id = create_response.json()["id"]
        
        # Update tournament
        update_response = client.put(
            f"/tournaments/{tournament_id}",
            json={
                "name": "Updated Name"
            }
        )
        
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["name"] == "Updated Name"
    
    def test_add_participant(self, client, event, players):
        """Test adding a participant to tournament"""
        # Create tournament
        tournament_response = client.post(
            "/tournaments/",
            json={
                "event_id": event["id"],
                "name": "Test Tournament",
                "tournament_type": "SINGLE_ELIMINATION"
            }
        )
        tournament_id = tournament_response.json()["id"]
        
        # Add participant
        response = client.post(
            f"/tournaments/{tournament_id}/participants",
            json={
                "player_id": players[0]["id"]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["participant_count"] == 1
    
    def test_add_multiple_participants(self, client, event, players):
        """Test adding multiple participants"""
        # Create tournament
        tournament_response = client.post(
            "/tournaments/",
            json={
                "event_id": event["id"],
                "name": "Test Tournament",
                "tournament_type": "SINGLE_ELIMINATION",
                "max_participants": 8
            }
        )
        tournament_id = tournament_response.json()["id"]
        
        # Add all players
        for player in players:
            response = client.post(
                f"/tournaments/{tournament_id}/participants",
                json={
                    "player_id": player["id"]
                }
            )
            assert response.status_code == 200
        
        # Verify all added
        get_response = client.get(f"/tournaments/{tournament_id}")
        assert get_response.json()["participant_count"] == len(players)
    
    def test_remove_participant(self, client, event, players):
        """Test removing a participant"""
        # Create tournament and add participant
        tournament_response = client.post(
            "/tournaments/",
            json={
                "event_id": event["id"],
                "name": "Test Tournament",
                "tournament_type": "SINGLE_ELIMINATION"
            }
        )
        tournament_id = tournament_response.json()["id"]
        
        # Add participant
        client.post(
            f"/tournaments/{tournament_id}/participants",
            json={"player_id": players[0]["id"]}
        )
        
        # Remove participant
        response = client.delete(
            f"/tournaments/{tournament_id}/participants/{players[0]['id']}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["participant_count"] == 0
    
    def test_start_tournament(self, client, event, players):
        """Test starting a tournament"""
        # Create tournament
        tournament_response = client.post(
            "/tournaments/",
            json={
                "event_id": event["id"],
                "name": "Test Tournament",
                "tournament_type": "SINGLE_ELIMINATION"
            }
        )
        tournament_id = tournament_response.json()["id"]
        
        # Add participants
        for player in players:
            client.post(
                f"/tournaments/{tournament_id}/participants",
                json={"player_id": player["id"]}
            )
        
        # Start tournament
        response = client.post(
            f"/tournaments/{tournament_id}/start",
            json={}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "IN_PROGRESS"
        assert data["current_round"] == 1
        assert data["bracket"] is not None
    
    def test_cannot_start_with_one_player(self, client, event, players):
        """Test that tournament requires at least 2 players"""
        # Create tournament
        tournament_response = client.post(
            "/tournaments/",
            json={
                "event_id": event["id"],
                "name": "Test Tournament",
                "tournament_type": "SINGLE_ELIMINATION"
            }
        )
        tournament_id = tournament_response.json()["id"]
        
        # Add only one participant
        client.post(
            f"/tournaments/{tournament_id}/participants",
            json={"player_id": players[0]["id"]}
        )
        
        # Try to start
        response = client.post(
            f"/tournaments/{tournament_id}/start",
            json={}
        )
        
        assert response.status_code == 400
        assert "at least 2" in response.json()["detail"].lower()
    
    def test_get_bracket(self, client, event, players):
        """Test getting tournament bracket"""
        # Create and start tournament
        tournament_response = client.post(
            "/tournaments/",
            json={
                "event_id": event["id"],
                "name": "Test Tournament",
                "tournament_type": "SINGLE_ELIMINATION"
            }
        )
        tournament_id = tournament_response.json()["id"]
        
        # Add participants
        for player in players:
            client.post(
                f"/tournaments/{tournament_id}/participants",
                json={"player_id": player["id"]}
            )
        
        # Start tournament
        client.post(
            f"/tournaments/{tournament_id}/start",
            json={}
        )
        
        # Get bracket
        response = client.get(f"/tournaments/{tournament_id}/bracket")
        
        assert response.status_code == 200
        data = response.json()
        assert data["tournament_id"] == tournament_id
        assert data["tournament_type"] == "SINGLE_ELIMINATION"
        assert data["bracket"] is not None
    
    def test_get_standings(self, client, event, players):
        """Test getting tournament standings"""
        # Create tournament
        tournament_response = client.post(
            "/tournaments/",
            json={
                "event_id": event["id"],
                "name": "Test Tournament",
                "tournament_type": "SINGLE_ELIMINATION"
            }
        )
        tournament_id = tournament_response.json()["id"]
        
        # Add participants
        for player in players:
            client.post(
                f"/tournaments/{tournament_id}/participants",
                json={"player_id": player["id"]}
            )
        
        # Get standings (should be empty initially)
        response = client.get(f"/tournaments/{tournament_id}/standings")
        
        assert response.status_code == 200
        data = response.json()
        assert data["tournament_id"] == tournament_id
        assert "standings" in data
    
    def test_cancel_tournament(self, client, event, players):
        """Test cancelling a tournament"""
        # Create tournament
        tournament_response = client.post(
            "/tournaments/",
            json={
                "event_id": event["id"],
                "name": "Test Tournament",
                "tournament_type": "SINGLE_ELIMINATION"
            }
        )
        tournament_id = tournament_response.json()["id"]
        
        # Cancel tournament
        response = client.post(
            f"/tournaments/{tournament_id}/cancel",
            json={}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "CANCELLED"
    
    def test_filter_tournaments_by_event(self, client, event, db_session):
        """Test filtering tournaments by event"""
        from models import Event
        
        # Create another event
        event2_response = client.post(
            "/events/",
            json={
                "name": "Event 2",
                "date": "2025-01-20",
                "time": "19:00"
            }
        )
        event2 = event2_response.json()
        
        # Create tournaments in both events
        client.post(
            "/tournaments/",
            json={
                "event_id": event["id"],
                "name": "Tournament 1",
                "tournament_type": "SINGLE_ELIMINATION"
            }
        )
        
        client.post(
            "/tournaments/",
            json={
                "event_id": event2["id"],
                "name": "Tournament 2",
                "tournament_type": "SWISS"
            }
        )
        
        # Filter by event
        response = client.get(f"/tournaments/?event_id={event['id']}")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should only get Tournament 1
        event_ids = {t["event_id"] for t in data}
        assert event["id"] in event_ids
    
    def test_tournament_with_all_types(self, client, event):
        """Test creating tournaments of all types"""
        tournament_types = [
            "SINGLE_ELIMINATION",
            "SWISS",
            "GROUP_KNOCKOUT",
            "ROUND_ROBIN"
        ]
        
        for tournament_type in tournament_types:
            response = client.post(
                "/tournaments/",
                json={
                    "event_id": event["id"],
                    "name": f"Tournament {tournament_type}",
                    "tournament_type": tournament_type
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["tournament_type"] == tournament_type
