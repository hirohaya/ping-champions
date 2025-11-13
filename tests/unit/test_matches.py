"""Unit tests for Match endpoints"""
import pytest
from fastapi import status


@pytest.mark.unit
@pytest.mark.api
class TestMatches:
    """Test Match API endpoints"""

    def test_create_match_success(self, client):
        """Test creating a new match"""
        # Create event
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        # Create players
        player1_response = client.post(
            "/players",
            json={"name": "João", "event_id": event_id}
        )
        player1_id = player1_response.json()["id"]
        
        player2_response = client.post(
            "/players",
            json={"name": "Maria", "event_id": event_id}
        )
        player2_id = player2_response.json()["id"]
        
        # Create match
        match_data = {
            "event_id": event_id,
            "player1_id": player1_id,
            "player2_id": player2_id,
            "best_of": 5
        }
        response = client.post("/matches", json=match_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["player1_id"] == player1_id
        assert data["player2_id"] == player2_id
        assert data["best_of"] == 5
        assert data["finished"] is False
        assert "id" in data

    def test_create_match_invalid_best_of(self, client):
        """Test creating match with invalid best_of value"""
        # Create event and players
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        player1_response = client.post(
            "/players",
            json={"name": "João", "event_id": event_id}
        )
        player1_id = player1_response.json()["id"]
        
        player2_response = client.post(
            "/players",
            json={"name": "Maria", "event_id": event_id}
        )
        player2_id = player2_response.json()["id"]
        
        # Try to create match with invalid best_of (4 is not valid)
        match_data = {
            "event_id": event_id,
            "player1_id": player1_id,
            "player2_id": player2_id,
            "best_of": 4
        }
        response = client.post("/matches", json=match_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_match_same_player(self, client):
        """Test creating match where player plays against themselves"""
        # Create event and player
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        player_response = client.post(
            "/players",
            json={"name": "João", "event_id": event_id}
        )
        player_id = player_response.json()["id"]
        
        # Try to create match with same player
        match_data = {
            "event_id": event_id,
            "player1_id": player_id,
            "player2_id": player_id,
            "best_of": 5
        }
        response = client.post("/matches", json=match_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_matches_in_event(self, client):
        """Test listing matches in an event"""
        # Create event
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        # Create players
        players = []
        for name in ["João", "Maria", "Pedro"]:
            player_response = client.post(
                "/players",
                json={"name": name, "event_id": event_id}
            )
            players.append(player_response.json()["id"])
        
        # Create matches
        match1_data = {
            "event_id": event_id,
            "player1_id": players[0],
            "player2_id": players[1]
        }
        client.post("/matches", json=match1_data)
        
        match2_data = {
            "event_id": event_id,
            "player1_id": players[1],
            "player2_id": players[2]
        }
        client.post("/matches", json=match2_data)
        
        # List matches
        response = client.get(f"/matches?event_id={event_id}")
        assert response.status_code == status.HTTP_200_OK
        matches = response.json()
        assert len(matches) == 2

    def test_get_match_success(self, client):
        """Test getting a specific match"""
        # Create event and players
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        player1_response = client.post(
            "/players",
            json={"name": "João", "event_id": event_id}
        )
        player1_id = player1_response.json()["id"]
        
        player2_response = client.post(
            "/players",
            json={"name": "Maria", "event_id": event_id}
        )
        player2_id = player2_response.json()["id"]
        
        # Create match
        match_data = {
            "event_id": event_id,
            "player1_id": player1_id,
            "player2_id": player2_id
        }
        match_response = client.post("/matches", json=match_data)
        match_id = match_response.json()["id"]
        
        # Get match
        response = client.get(f"/matches/{match_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == match_id
        assert data["player1_id"] == player1_id
        assert data["player2_id"] == player2_id

    def test_update_match_winner(self, client):
        """Test updating a match with winner"""
        # Create event and players
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        player1_response = client.post(
            "/players",
            json={"name": "João", "event_id": event_id}
        )
        player1_id = player1_response.json()["id"]
        
        player2_response = client.post(
            "/players",
            json={"name": "Maria", "event_id": event_id}
        )
        player2_id = player2_response.json()["id"]
        
        # Create match
        match_data = {
            "event_id": event_id,
            "player1_id": player1_id,
            "player2_id": player2_id
        }
        match_response = client.post("/matches", json=match_data)
        match_id = match_response.json()["id"]
        
        # Update match with winner
        update_data = {
            "winner_id": player1_id,
            "finished": True
        }
        response = client.put(f"/matches/{match_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["winner_id"] == player1_id
        assert data["finished"] is True

    def test_update_match_invalid_winner(self, client):
        """Test updating match with winner not in the match"""
        # Create event and players
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        player1_response = client.post(
            "/players",
            json={"name": "João", "event_id": event_id}
        )
        player1_id = player1_response.json()["id"]
        
        player2_response = client.post(
            "/players",
            json={"name": "Maria", "event_id": event_id}
        )
        player2_id = player2_response.json()["id"]
        
        player3_response = client.post(
            "/players",
            json={"name": "Pedro", "event_id": event_id}
        )
        player3_id = player3_response.json()["id"]
        
        # Create match
        match_data = {
            "event_id": event_id,
            "player1_id": player1_id,
            "player2_id": player2_id
        }
        match_response = client.post("/matches", json=match_data)
        match_id = match_response.json()["id"]
        
        # Try to set winner not in the match
        update_data = {
            "winner_id": player3_id
        }
        response = client.put(f"/matches/{match_id}", json=update_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_match_success(self, client):
        """Test deleting a match"""
        # Create event and players
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        player1_response = client.post(
            "/players",
            json={"name": "João", "event_id": event_id}
        )
        player1_id = player1_response.json()["id"]
        
        player2_response = client.post(
            "/players",
            json={"name": "Maria", "event_id": event_id}
        )
        player2_id = player2_response.json()["id"]
        
        # Create match
        match_data = {
            "event_id": event_id,
            "player1_id": player1_id,
            "player2_id": player2_id
        }
        match_response = client.post("/matches", json=match_data)
        match_id = match_response.json()["id"]
        
        # Delete match
        response = client.delete(f"/matches/{match_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify match is deleted
        list_response = client.get(f"/matches?event_id={event_id}")
        matches = list_response.json()
        assert len(matches) == 0

    def test_delete_match_not_found(self, client):
        """Test deleting non-existent match"""
        response = client.delete("/matches/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
