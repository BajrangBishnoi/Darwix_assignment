from datetime import datetime
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.database import SessionLocal
from app.main import app
from app.models import Call

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_call_not_found():
    response = client.get("/api/v1/calls/nonexistent-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Call not found"}


def test_get_call_success():
    fake_call = Call(
        call_id="abc123",
        agent_id="agent001",
        customer_id="cust001",
        language="en",
        start_time="2023-08-01T10:00:00",
        duration_seconds=300,
        transcript="Test call transcript",
        sentiment_score=0.75,
        agent_talk_ratio=0.6,
    )

    with patch("app.crud.CallService.get_call_by_id", return_value=fake_call):
        response = client.get("/api/v1/calls/abc123")
        assert response.status_code == 200
        data = response.json()
        assert data["call_id"] == "abc123"
        assert data["agent_id"] == "agent001"


def test_get_call_by_id():

    db = SessionLocal()
    mock_call = Call(
        call_id="test-call-id-20",
        agent_id="agent-1",
        customer_id="cust_1",
        language="en",
        start_time=datetime.now(),
        transcript="Hello world",
        sentiment_score=0.5,
        agent_talk_ratio=0.6,
    )
    db.add(mock_call)
    db.commit()

    response = client.get("/api/v1/calls/test-call-id-20")
    assert response.status_code == 200
    data = response.json()
    assert data["call_id"] == "test-call-id-20"

    db.delete(mock_call)
    db.commit()
    db.close()


def test_get_all_calls():
    response = client.get("/api/v1/calls")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_recommendations():
    db = SessionLocal()
    mock_call = Call(
        call_id="test-call-id-20",
        agent_id="agent-1",
        customer_id="cust_1",
        language="en",
        start_time=datetime.now(),
        transcript="This is a test transcript",
        sentiment_score=0.6,
        agent_talk_ratio=0.7,
    )
    db.add(mock_call)
    db.commit()

    response = client.get("/api/v1/calls/test-call-id-2/recommendations")
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, dict)

    db.delete(mock_call)
    db.commit()
    db.close()


def test_get_agent_analytics():
    response = client.get("/api/v1/analytics/agents")
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)
