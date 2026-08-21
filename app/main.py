"""
URL Shortener API — FastAPI + PostgreSQL.

Endpoints:
    POST /shorten       → Accept a long URL, return a shortened URL.
    GET  /{short_code}  → Redirect to the original URL (HTTP 307).
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.crud import create_short_url, get_url_by_short_code
from app.database import Base, engine, get_db
from app.schemas import URLCreate, URLResponse


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Create tables on startup (use Alembic in production)."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="URL Shortener API",
    description="A URL shortening service built with FastAPI and PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(url_in: URLCreate, db: Session = Depends(get_db)) -> URLResponse:
    """Accept a long URL and return a shortened URL."""
    db_url = create_short_url(db=db, url=url_in)
    short_url = f"{settings.base_url.rstrip('/')}/{db_url.short_code}"
    return URLResponse(short_code=db_url.short_code, short_url=short_url)


@app.get("/{short_code}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
def redirect_to_url(short_code: str, db: Session = Depends(get_db)) -> RedirectResponse:
    """Look up the short code and redirect to the original URL. Returns 404 if not found."""
    db_url = get_url_by_short_code(db=db, short_code=short_code)
    if db_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found",
        )
    return RedirectResponse(url=db_url.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
