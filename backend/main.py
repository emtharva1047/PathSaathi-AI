"""FastAPI application entrypoint."""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.routes.health import router as health_router
from core.config import settings
from core.logging_config import configure_logging


configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=f"{settings.app_name} API",
    version="0.1.0",
    description="API for bilingual vocational counselling and family decision support.",
)
app.include_router(health_router)


@app.exception_handler(Exception)
async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
    """Return a generic error without exposing internal details to API clients."""
    logger.error("Unhandled API error on %s", request.url.path, exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected server error occurred."},
    )
