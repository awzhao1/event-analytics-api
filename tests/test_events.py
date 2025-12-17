# tests/test_events.py
import uuid
from datetime import datetime, timedelta

def test_create_event(client, test_user):
    # Create a new event
    response = client.post(
        "/events/",
        headers={"X-API-Key": test_user.api_key},
        json={
            "event_type": "page_view",
            "event_metadata": {"page": "/home"}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data

def test_create_event_invalid_api_key(client):
    # Attempt to create event with invalid API key
    response = client.post(
        "/events/",
        headers={"X-API-Key": "invalid_key"},
        json={"event_type": "page_view"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid API key"}

def test_event_summary(client, test_user):
    # Create a few events first
    client.post(
        "/events/",
        headers={"X-API-Key": test_user.api_key},
        json={"event_type": "signup"}
    )
    client.post(
        "/events/",
        headers={"X-API-Key": test_user.api_key},
        json={"event_type": "page_view"}
    )

    # Fetch summary
    response = client.get(
        "/events/summary",
        headers={"X-API-Key": test_user.api_key}
    )
    assert response.status_code == 200
    data = response.json()

    # At least one page_view and one signup
    event_types = [d["event_type"] for d in data]
    assert "page_view" in event_types
    assert "signup" in event_types

def test_event_summary_time_window(client, test_user):
    now = datetime.utcnow()
    past = now - timedelta(days=1)
    future = now + timedelta(days=1)

    # Create an event now
    client.post(
        "/events/",
        headers={"X-API-Key": test_user.api_key},
        json={"event_type": "page_view"}
    )

    # Query with start in the future → should return empty
    response = client.get(
        f"/events/summary?start={future.isoformat()}",
        headers={"X-API-Key": test_user.api_key}
    )
    assert response.status_code == 200
    assert response.json() == []

    # Query with start in the past → should include our event
    response = client.get(
        f"/events/summary?start={past.isoformat()}",
        headers={"X-API-Key": test_user.api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert any(d["event_type"] == "page_view" for d in data)
