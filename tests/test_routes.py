"""Tests for API routes."""

import json


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"


def test_calculate_endpoint(client):
    """Test calculate endpoint."""
    payload = {"amount": 100, "tax_rate": 0.1}
    response = client.post(
        "/api/calculate", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["total"] == 110.0


def test_validate_email_endpoint(client):
    """Test email validation endpoint."""
    # Valid email
    payload = {"email": "test@example.com"}
    response = client.post(
        "/api/validate-email",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["is_valid"] is True

    # Invalid email
    payload = {"email": "invalid-email"}
    response = client.post(
        "/api/validate-email",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["is_valid"] is False


def test_get_user_found(client):
    """Test get user endpoint with existing user."""
    response = client.get("/api/users/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == 1
    assert data["name"] == "Alice"


def test_get_user_not_found(client):
    """Test get user endpoint with non-existing user."""
    response = client.get("/api/users/999")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
