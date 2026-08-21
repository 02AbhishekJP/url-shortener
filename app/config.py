"""Application settings loaded from environment variables."""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


def _resolve_base_url() -> str:
    """Auto-detect the public base URL from Render, Netlify, or fall back to localhost."""
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if render_url:
        return render_url
    netlify_url = os.getenv("URL")
    if netlify_url:
        return netlify_url
    return os.getenv("BASE_URL", "http://localhost:8000")



def _resolve_database_url() -> str:
    """Detect DATABASE_URL from environment or fall back to SQLite if not set."""
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url
    if os.getenv("NETLIFY") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        return "sqlite:////tmp/url_shortener.db"
    return "sqlite:///./url_shortener.db"


class Settings(BaseSettings):
    database_url: str = _resolve_database_url()
    base_url: str = _resolve_base_url()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
