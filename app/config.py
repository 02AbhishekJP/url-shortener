"""Application settings loaded from environment variables."""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


def _resolve_base_url() -> str:
    """Auto-detect the public base URL from Railway or fall back to localhost."""
    railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    if railway_domain:
        return f"https://{railway_domain}"
    return os.getenv("BASE_URL", "http://localhost:8000")


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/url_shortener"
    base_url: str = _resolve_base_url()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
