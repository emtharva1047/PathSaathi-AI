"""Environment-backed application settings."""
from __future__ import annotations

import os
from dataclasses import dataclass, field

DEFAULT_DATABASE_URL = "sqlite:///./data/pathsaathi.db"


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings; local SQLite is the safe default for development."""

    app_name: str = field(default_factory=lambda: os.getenv("APP_NAME", "PathSaathi AI"))
    app_env: str = field(default_factory=lambda: os.getenv("APP_ENV", "development"))
    api_host: str = field(default_factory=lambda: os.getenv("API_HOST", "127.0.0.1"))
    api_port: int = field(default_factory=lambda: int(os.getenv("API_PORT", "8000")))
    database_url: str = field(
        default_factory=lambda: os.getenv("PATHSAATHI_DATABASE_URL", DEFAULT_DATABASE_URL)
    )
    database_echo: bool = field(
        default_factory=lambda: os.getenv("DATABASE_ECHO", "false").strip().lower()
        in {"1", "true", "yes"}
    )


settings = Settings()