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



class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/url_shortener"
    base_url: str = _resolve_base_url()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
