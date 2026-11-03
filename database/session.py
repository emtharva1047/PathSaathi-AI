"""SQLAlchemy engine and session helpers for local SQLite/PostgreSQL URLs."""
from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from core.config import settings
from database.base import Base


def create_database_engine(
    database_url: str | None = None,
    *,
    echo: bool | None = None,
) -> Engine:
    """Create an engine from configuration; no connection is opened at import time."""
    url_text = database_url or settings.database_url
    url = make_url(url_text)
    options: dict[str, object] = {
        "echo": settings.database_echo if echo is None else echo,
        "pool_pre_ping": True,
    }

    if url.get_backend_name() == "sqlite":
        options["connect_args"] = {"check_same_thread": False}
        if url.database in {None, "", ":memory:"}:
            options["poolclass"] = StaticPool
        elif not url.database.startswith("file:"):
            database_path = Path(url.database).expanduser()
            if not database_path.is_absolute():
                database_path = Path.cwd() / database_path
            database_path.parent.mkdir(parents=True, exist_ok=True)

    return create_engine(url, **options)


def create_schema(engine: Engine) -> None:
    """Create local development tables explicitly; never called on module import."""
    from database import models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Build a session factory; transaction commit/rollback stays with the caller."""
    return sessionmaker(
        bind=engine,
        class_=Session,
        autoflush=False,
        expire_on_commit=False,
    )


def get_session(session_factory: sessionmaker[Session]) -> Iterator[Session]:
    """Yield a short-lived session suitable for a FastAPI dependency."""
    with session_factory() as session:
        yield session