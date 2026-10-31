"""FastAPI application entrypoint."""

from fastapi import FastAPI

from backend.routes.health import router as health_router
from core.config import settings


app = FastAPI(
    title=f"{settings.app_name} API",
    version="0.1.0",
    description="API for bilingual vocational counselling and family decision support.",
)
app.include_router(health_router)
