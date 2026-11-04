"""FastAPI application entrypoint."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.dependencies import dispose_database
from backend.routes.catalogue import router as catalogue_router
from backend.routes.health import router as health_router
from core.config import settings
from core.logging_config import configure_logging


configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Release a database engine if a request created one; do not initialise schema."""
    try:
        yield
    finally:
        dispose_database()


app = FastAPI(
    title=f"{settings.app_name} API",
    version="0.1.0",
    description="API for bilingual vocational counselling and family decision support.",
    lifespan=lifespan,
)
app.include_router(health_router)
app.include_router(catalogue_router)


@app.exception_handler(Exception)
async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
    """Return a generic error without exposing internal details to API clients."""
    logger.error("Unhandled API error on %s (%s)", request.url.path, type(exc).__name__)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected server error occurred."},
    )
