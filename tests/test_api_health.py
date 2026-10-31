"""Smoke tests for the FastAPI health endpoint without deprecated TestClient usage."""

import asyncio

import httpx

from backend.main import app


async def request_health() -> httpx.Response:
    """Call the ASGI app through an in-process HTTP transport."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.get("/health")


def test_health_endpoint_returns_service_status() -> None:
    response = asyncio.run(request_health())

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "pathsaathi-api"}
