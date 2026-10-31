"""Health-check route."""

from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Stable health-check response."""

    status: str
    service: str


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return API process health without depending on external services."""
    return HealthResponse(status="ok", service="pathsaathi-api")
