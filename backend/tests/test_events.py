"""Unit tests for Event endpoints"""
import pytest
from fastapi import status


@pytest.mark.unit
@pytest.mark.api
class TestEvents:
    """Test Event API endpoints"""

    def test_list_events_empty(self, client):
        """Test listing events when database is empty"""
        response = client.get("/events")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_event_success(self, client):
        """Test creating a new event with valid data"""
        event_data = {
            "name": "Tournament 2024",
            "date": "2024-12-15",
            "time": "19:00"
        }
        response = client.post("/events", json=event_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == event_data["name"]
        assert data["date"] == event_data["date"]
        assert data["time"] == event_data["time"]
        assert data["active"] is True
        assert "id" in data

    def test_create_event_invalid_date_format(self, client):
        """Test creating event with invalid date format"""
        event_data = {
            "name": "Tournament 2024",
            "date": "15-12-2024",  # Wrong format
            "time": "19:00"
        }
        response = client.post("/events", json=event_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_event_invalid_time_format(self, client):
        """Test creating event with invalid time format"""
        event_data = {
            "name": "Tournament 2024",
            "date": "2024-12-15",
            "time": "7:00 PM"  # Wrong format
        }
        response = client.post("/events", json=event_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_event_missing_name(self, client):
        """Test creating event without name"""
        event_data = {
            "date": "2024-12-15",
            "time": "19:00"
        }
        response = client.post("/events", json=event_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_list_events_with_data(self, client):
        """Test listing events after creating some"""
        # Create first event
        event1 = {
            "name": "Tournament 1",
            "date": "2024-12-15",
            "time": "19:00"
        }
        client.post("/events", json=event1)
        
        # Create second event
        event2 = {
            "name": "Tournament 2",
            "date": "2024-12-16",
            "time": "20:00"
        }
        client.post("/events", json=event2)
        
        # List events
        response = client.get("/events")
        assert response.status_code == status.HTTP_200_OK
        events = response.json()
        assert len(events) == 2
        assert events[0]["name"] == event1["name"]
        assert events[1]["name"] == event2["name"]

    def test_get_event_success(self, client):
        """Test getting a specific event"""
        # Create event
        event_data = {
            "name": "Test Event",
            "date": "2024-12-15",
            "time": "19:00"
        }
        create_response = client.post("/events", json=event_data)
        event_id = create_response.json()["id"]
        
        # Get event
        response = client.get(f"/events/{event_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == event_id
        assert data["name"] == event_data["name"]

    def test_get_event_not_found(self, client):
        """Test getting non-existent event"""
        response = client.get("/events/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_event_success(self, client):
        """Test soft deleting an event"""
        # Create event
        event_data = {
            "name": "Event to Delete",
            "date": "2024-12-15",
            "time": "19:00"
        }
        create_response = client.post("/events", json=event_data)
        event_id = create_response.json()["id"]
        
        # Delete event
        response = client.delete(f"/events/{event_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify event is not in list anymore
        list_response = client.get("/events")
        events = list_response.json()
        assert len(events) == 0

    def test_delete_event_not_found(self, client):
        """Test deleting non-existent event"""
        response = client.delete("/events/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
