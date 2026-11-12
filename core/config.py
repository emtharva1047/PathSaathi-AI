"""Environment-backed application settings with fail-fast validation."""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError

DEFAULT_DATABASE_URL = "sqlite:///./data/pathsaathi.db"
_TRUE_VALUES = {"1", "true", "yes", "on"}
_FALSE_VALUES = {"0", "false", "no", "off"}


def _read_text_env(name: str, default: str) -> str:
    """Read a required environment value and reject whitespace-only input."""
    value = os.getenv(name, default)
    if not value.strip():
        raise ValueError(f"{name} must not be blank.")
    return value.strip()


def _read_api_port() -> int:
    """Parse and validate the API port from the environment."""
    raw_value = _read_text_env("API_PORT", "8000")
    try:
        port = int(raw_value)
    except ValueError as exc:
        raise ValueError("API_PORT must be an integer between 1 and 65535.") from exc
    _validate_api_port(port)
    return port


def _validate_api_port(port: int) -> None:
    """Reject booleans, non-integers and ports outside the TCP range."""
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("API_PORT must be an integer between 1 and 65535.")


def _read_bool_env(name: str, default: str) -> bool:
    """Parse explicit boolean tokens rather than silently treating typos as false."""
    value = _read_text_env(name, default).lower()
    if value in _TRUE_VALUES:
        return True
    if value in _FALSE_VALUES:
        return False
    raise ValueError(f"{name} must be one of: true, false, 1, 0, yes, no, on or off.")


def _validate_database_url(database_url: str) -> str:
    """Validate supported synchronous SQLAlchemy URL syntax without connecting."""
    if not isinstance(database_url, str) or not database_url.strip():
        raise ValueError("PATHSAATHI_DATABASE_URL must not be blank.")

    normalized_url = database_url.strip()
    try:
        url = make_url(normalized_url)
    except (ArgumentError, TypeError, ValueError) as exc:
        raise ValueError("PATHSAATHI_DATABASE_URL must be a valid SQLAlchemy URL.") from exc

    if url.get_backend_name() not in {"sqlite", "postgresql"}:
        raise ValueError("PATHSAATHI_DATABASE_URL must use SQLite or PostgreSQL.")

    if url.get_backend_name() == "postgresql" and not url.host:
        raise ValueError("PATHSAATHI_DATABASE_URL must include a PostgreSQL host.")

    return normalized_url


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings; local SQLite is the safe default for development."""

    app_name: str = field(default_factory=lambda: _read_text_env("APP_NAME", "PathSaathi AI"))
    app_env: str = field(default_factory=lambda: _read_text_env("APP_ENV", "development"))
    api_host: str = field(default_factory=lambda: _read_text_env("API_HOST", "127.0.0.1"))
    api_port: int = field(default_factory=_read_api_port)
    database_url: str = field(
        default_factory=lambda: _read_text_env("PATHSAATHI_DATABASE_URL", DEFAULT_DATABASE_URL)
    )
    database_echo: bool = field(default_factory=lambda: _read_bool_env("DATABASE_ECHO", "false"))

    def __post_init__(self) -> None:
        """Fail fast on invalid settings before the application starts serving requests."""
        for name in ("app_name", "app_env", "api_host"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name.upper()} must not be blank.")
            if name == "api_host" and any(character.isspace() for character in value):
                raise ValueError("API_HOST must not contain whitespace.")
            object.__setattr__(self, name, value.strip())

        _validate_api_port(self.api_port)
        if not isinstance(self.database_echo, bool):
            raise ValueError("DATABASE_ECHO must be a boolean.")
        object.__setattr__(self, "database_url", _validate_database_url(self.database_url))


settings = Settings()
