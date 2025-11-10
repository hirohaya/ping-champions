"""Unit tests for Player endpoints"""
import pytest
from fastapi import status


@pytest.mark.unit
@pytest.mark.api
class TestPlayers:
    """Test Player API endpoints"""

    def test_list_players_empty(self, client):
        """Test listing players when database is empty"""
        response = client.get("/players?event_id=1")
        assert response.status_code == status.HTTP_404_NOT_FOUND  # Event doesn't exist

    def test_register_player_success(self, client):
        """Test registering a new player"""
        # Create event first
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        # Register player
        player_data = {
            "name": "João Silva",
            "event_id": event_id
        }
        response = client.post("/players", json=player_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == player_data["name"]
        assert data["event_id"] == event_id
        assert "id" in data

    def test_register_player_nonexistent_event(self, client):
        """Test registering player for non-existent event"""
        player_data = {
            "name": "João Silva",
            "event_id": 999
        }
        response = client.post("/players", json=player_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_register_player_invalid_name(self, client):
        """Test registering player with empty name"""
        # Create event first
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        # Try to register with empty name
        player_data = {
            "name": "",
            "event_id": event_id
        }
        response = client.post("/players", json=player_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_list_players_in_event(self, client):
        """Test listing players in an event"""
        # Create event
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        # Register players
        for name in ["João", "Maria", "Pedro"]:
            player_data = {"name": name, "event_id": event_id}
            client.post("/players", json=player_data)
        
        # List players
        response = client.get(f"/players?event_id={event_id}")
        assert response.status_code == status.HTTP_200_OK
        players = response.json()
        assert len(players) == 3

    def test_get_player_success(self, client):
        """Test getting a specific player"""
        # Create event and player
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        player_data = {"name": "João Silva", "event_id": event_id}
        player_response = client.post("/players", json=player_data)
        player_id = player_response.json()["id"]
        
        # Get player
        response = client.get(f"/players/{player_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == player_id
        assert data["name"] == "João Silva"

    def test_get_player_not_found(self, client):
        """Test getting non-existent player"""
        response = client.get("/players/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_player_success(self, client):
        """Test updating a player"""
        # Create event and player
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        player_data = {"name": "João Silva", "event_id": event_id}
        player_response = client.post("/players", json=player_data)
        player_id = player_response.json()["id"]
        
        # Update player
        update_data = {
            "name": "João Silva Updated",
            "score": 100
        }
        response = client.put(f"/players/{player_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "João Silva Updated"
        assert data["score"] == 100

    def test_delete_player_success(self, client):
        """Test soft deleting a player"""
        # Create event and player
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        player_data = {"name": "João Silva", "event_id": event_id}
        player_response = client.post("/players", json=player_data)
        player_id = player_response.json()["id"]
        
        # Delete player
        response = client.delete(f"/players/{player_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify player is not in event list
        list_response = client.get(f"/players?event_id={event_id}")
        players = list_response.json()
        assert len(players) == 0

    def test_list_all_players(self, client):
        """Test listing all players including inactive"""
        # Create event and players
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        # Create and delete a player
        player_data = {"name": "João", "event_id": event_id}
        player_response = client.post("/players", json=player_data)
        player_id = player_response.json()["id"]
        client.delete(f"/players/{player_id}")
        
        # Create another player
        player_data2 = {"name": "Maria", "event_id": event_id}
        client.post("/players", json=player_data2)
        
        # List all players
        response = client.get("/players/all")
        assert response.status_code == status.HTTP_200_OK
        players = response.json()
        assert len(players) == 2  # Both active and inactive
