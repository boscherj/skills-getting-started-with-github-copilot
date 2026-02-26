"""Tests for activities endpoints."""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Check that all expected activities are present
    expected_activities = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Studio",
        "Drama Club",
        "Debate Team",
        "Science Club"
    }
    assert set(activities.keys()) == expected_activities


def test_get_activities_returns_correct_structure(client):
    """Test that activities have the correct structure."""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_details in activities.items():
        assert "description" in activity_details
        assert "schedule" in activity_details
        assert "max_participants" in activity_details
        assert "participants" in activity_details
        
        # Validate types
        assert isinstance(activity_details["description"], str)
        assert isinstance(activity_details["schedule"], str)
        assert isinstance(activity_details["max_participants"], int)
        assert isinstance(activity_details["participants"], list)


def test_get_activities_participants_are_email_strings(client):
    """Test that participants are strings (email addresses)."""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_details in activities.items():
        for participant in activity_details["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant, f"Participant {participant} should be an email address"
