"""Unit tests for Ranking endpoints"""
import pytest
from fastapi import status


@pytest.mark.unit
@pytest.mark.api
class TestRanking:
    """Test Ranking API endpoints"""

    def test_ranking_empty_event(self, client):
        """Test ranking for event with no players"""
        # Create event
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        # Get ranking
        response = client.get(f"/ranking?event_id={event_id}")
        assert response.status_code == status.HTTP_200_OK
        ranking = response.json()
        assert ranking == []

    def test_ranking_no_matches(self, client):
        """Test ranking for event with players but no matches"""
        # Create event
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        # Create players
        for name in ["João", "Maria", "Pedro"]:
            client.post("/players", json={"name": name, "event_id": event_id})
        
        # Get ranking
        response = client.get(f"/ranking?event_id={event_id}")
        assert response.status_code == status.HTTP_200_OK
        ranking = response.json()
        assert len(ranking) == 3
        # All should have 0 wins
        for entry in ranking:
            assert entry["wins"] == 0
            assert entry["losses"] == 0
            assert entry["win_rate"] == 0.0

    def test_ranking_with_matches(self, client):
        """Test ranking calculation with finished matches"""
        # Create event
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = client.post("/events", json=event_data)
        event_id = event_response.json()["id"]
        
        # Create players
        player_names = ["João", "Maria", "Pedro"]
        players = []
        for name in player_names:
            player_response = client.post(
                "/players",
                json={"name": name, "event_id": event_id}
            )
            players.append(player_response.json())
        
        # Create and finish matches
        # João beats Maria
        match1_data = {
            "event_id": event_id,
            "player1_id": players[0]["id"],
            "player2_id": players[1]["id"]
        }
        match1_response = client.post("/matches", json=match1_data)
        match1_id = match1_response.json()["id"]
        client.put(
            f"/matches/{match1_id}",
            json={"winner_id": players[0]["id"], "finished": True}
        )
        
        # Maria beats Pedro
        match2_data = {
            "event_id": event_id,
            "player1_id": players[1]["id"],
            "player2_id": players[2]["id"]
        }
        match2_response = client.post("/matches", json=match2_data)
        match2_id = match2_response.json()["id"]
        client.put(
            f"/matches/{match2_id}",
            json={"winner_id": players[1]["id"], "finished": True}
        )
        
        # Get ranking
        response = client.get(f"/ranking?event_id={event_id}")
        assert response.status_code == status.HTTP_200_OK
        ranking = response.json()
        assert len(ranking) == 3
        
        # João should be first with 1 win
        assert ranking[0]["name"] == "João"
        assert ranking[0]["wins"] == 1
        assert ranking[0]["losses"] == 0
        assert ranking[0]["win_rate"] == 1.0
        
        # Maria should be second with 1 win, 1 loss
        assert ranking[1]["name"] == "Maria"
        assert ranking[1]["wins"] == 1
        assert ranking[1]["losses"] == 1
        assert ranking[1]["win_rate"] == 0.5
        
        # Pedro should be last with 0 wins, 1 loss
        assert ranking[2]["name"] == "Pedro"
        assert ranking[2]["wins"] == 0
        assert ranking[2]["losses"] == 1
        assert ranking[2]["win_rate"] == 0.0

    def test_ranking_nonexistent_event(self, client):
        """Test ranking for non-existent event"""
        response = client.get("/ranking?event_id=999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_ranking_sorting(self, client):
        """Test that ranking is sorted correctly"""
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
            players.append(player_response.json())
        
        # Create multiple matches to establish clear ranking
        # Match 1: João beats Maria
        match1 = client.post(
            "/matches",
            json={
                "event_id": event_id,
                "player1_id": players[0]["id"],
                "player2_id": players[1]["id"]
            }
        ).json()
        client.put(
            f"/matches/{match1['id']}",
            json={"winner_id": players[0]["id"], "finished": True}
        )
        
        # Match 2: João beats Pedro
        match2 = client.post(
            "/matches",
            json={
                "event_id": event_id,
                "player1_id": players[0]["id"],
                "player2_id": players[2]["id"]
            }
        ).json()
        client.put(
            f"/matches/{match2['id']}",
            json={"winner_id": players[0]["id"], "finished": True}
        )
        
        # Match 3: Maria beats Pedro
        match3 = client.post(
            "/matches",
            json={
                "event_id": event_id,
                "player1_id": players[1]["id"],
                "player2_id": players[2]["id"]
            }
        ).json()
        client.put(
            f"/matches/{match3['id']}",
            json={"winner_id": players[1]["id"], "finished": True}
        )
        
        # Get ranking
        response = client.get(f"/ranking?event_id={event_id}")
        ranking = response.json()
        
        # Check order: João (2 wins), Maria (1 win), Pedro (0 wins)
        assert ranking[0]["wins"] == 2
        assert ranking[1]["wins"] == 1
        assert ranking[2]["wins"] == 0
