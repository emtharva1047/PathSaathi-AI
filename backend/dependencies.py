"""Lazy, request-scoped SQLAlchemy dependency for FastAPI."""

from __future__ import annotations

from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from database.session import create_database_engine, create_session_factory


@lru_cache(maxsize=1)
def _get_engine() -> Engine:
    """Create one engine on first database use, never during module import."""
    return create_database_engine()


@lru_cache(maxsize=1)
def _get_session_factory() -> sessionmaker[Session]:
    """Reuse a session factory while keeping individual sessions request-scoped."""
    return create_session_factory(_get_engine())


def get_db_session() -> Iterator[Session]:
    """Yield a short-lived session; this read-only API leaves commits to services."""
    with _get_session_factory()() as session:
        yield session


def dispose_database() -> None:
    """Dispose the lazily created engine during application shutdown."""
    if _get_engine.cache_info().currsize:
        _get_engine().dispose()
    _get_session_factory.cache_clear()
    _get_engine.cache_clear()
