"""Smoke tests for the FastAPI health endpoint."""

from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health_endpoint_returns_service_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "pathsaathi-api"}
