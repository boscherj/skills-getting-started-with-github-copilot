"""Tests for participant management endpoints (signup and removal)."""

import pytest


class TestSignup:
    """Tests for the signup endpoint."""
    
    def test_signup_successful(self, client):
        """Test successful signup for an activity."""
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]
        assert activity in response.json()["message"]
    
    
    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup actually adds the participant to the activity list."""
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        
        # Signup
        client.post(f"/activities/{activity}/signup", params={"email": email})
        
        # Get activities and verify participant was added
        response = client.get("/activities")
        activities = response.json()
        
        assert email in activities[activity]["participants"]
    
    
    def test_signup_duplicate_registration_fails(self, client):
        """Test that a student cannot sign up for an activity twice."""
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        
        # First signup should succeed
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second signup should fail
        response2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"]
    
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        """Test that signing up for a non-existent activity returns 404."""
        email = "student@mergington.edu"
        activity = "NonExistent Club"
        
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    
    def test_signup_with_special_characters_in_email(self, client):
        """Test signup with email containing special characters."""
        email = "student+test@mergington.edu"
        activity = "Chess Club"
        
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        assert response.status_code == 200
        
        # Verify participant was added
        response = client.get("/activities")
        activities = response.json()
        assert email in activities[activity]["participants"]


class TestRemoveParticipant:
    """Tests for the remove participant endpoint."""
    
    def test_remove_participant_successful(self, client):
        """Test successful removal of a participant."""
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"
        
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        assert email in response.json()["message"]
        assert activity in response.json()["message"]
    
    
    def test_remove_participant_removes_from_list(self, client):
        """Test that removal actually removes the participant from the activity."""
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"
        
        # Remove participant
        client.delete(f"/activities/{activity}/participants/{email}")
        
        # Get activities and verify participant was removed
        response = client.get("/activities")
        activities = response.json()
        
        assert email not in activities[activity]["participants"]
    
    
    def test_remove_nonexistent_participant_returns_404(self, client):
        """Test that removing a non-existent participant returns 404."""
        email = "nonexistent@mergington.edu"
        activity = "Chess Club"
        
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]
    
    
    def test_remove_from_nonexistent_activity_returns_404(self, client):
        """Test that removing from a non-existent activity returns 404."""
        email = "student@mergington.edu"
        activity = "NonExistent Club"
        
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    
    def test_remove_then_signup_again(self, client):
        """Test that a participant can signup again after being removed."""
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        
        # Signup
        client.post(f"/activities/{activity}/signup", params={"email": email})
        
        # Remove
        client.delete(f"/activities/{activity}/participants/{email}")
        
        # Signup again - should succeed
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify participant is in the list
        response = client.get("/activities")
        activities = response.json()
        assert email in activities[activity]["participants"]


class TestSignupWithRemoval:
    """Integration tests for signup and removal workflows."""
    
    def test_multiple_signups_and_removals(self, client):
        """Test complex scenario with multiple signups and removals."""
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        activity = "Art Studio"
        
        # Both students signup
        client.post(f"/activities/{activity}/signup", params={"email": email1})
        client.post(f"/activities/{activity}/signup", params={"email": email2})
        
        # Verify both are in the list
        response = client.get("/activities")
        participants = response.json()[activity]["participants"]
        assert email1 in participants
        assert email2 in participants
        
        # Remove first student
        client.delete(f"/activities/{activity}/participants/{email1}")
        
        # Verify first is removed but second remains
        response = client.get("/activities")
        participants = response.json()[activity]["participants"]
        assert email1 not in participants
        assert email2 in participants
    
    
    def test_signup_to_different_activities(self, client):
        """Test that a student can be in the duplicate check across multiple activities."""
        email = "newstudent@mergington.edu"
        
        # Signup to first activity
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Try to signup to second activity - should fail due to duplicate check
        response2 = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"]
