"""Tests for authentication and root endpoints."""


def test_root_redirects_to_static_index(client):
    """Test that GET / redirects to the static index.html file."""
    response = client.get("/", follow_redirects=False)
    
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_with_follow(client):
    """Test that following the redirect from / reaches static content."""
    response = client.get("/", follow_redirects=True)
    
    # The response should be the HTML content or a 200 status
    # (static file serving might have different status codes)
    assert response.status_code == 200
