"""Environment-backed application settings."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the API process."""

    app_name: str = os.getenv("APP_NAME", "PathSaathi AI")
    app_env: str = os.getenv("APP_ENV", "development")
    api_host: str = os.getenv("API_HOST", "127.0.0.1")
    api_port: int = int(os.getenv("API_PORT", "8000"))


settings = Settings()
