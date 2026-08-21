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


# Create database tables at module import time
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Startup DB Warning: {e}")


description = """
A powerful and lightweight URL Shortening service. 🚀

## Features
* **Shorten URLs**: Submit any valid long URL and receive a compact, shareable short link.
* **Instant Redirection**: Navigate to the short link and get instantly redirected to the original destination.
* **Collision-Safe**: Built-in mechanisms to prevent short code duplication.
"""

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="LOBB URL Shortener API",
    description=description,
    docs_url="/docs",
)


@app.get("", include_in_schema=False)
@app.get("/", include_in_schema=False)
def root_redirect():
    """Redirect to the API documentation."""
    return RedirectResponse(url="/docs")


@app.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED, tags=["URLs"])
def shorten_url(url_in: URLCreate, db: Session = Depends(get_db)) -> URLResponse:
    """Accept a long URL and return a shortened URL."""
    db_url = create_short_url(db=db, url=url_in)
    short_url = f"{settings.base_url.rstrip('/')}/{db_url.short_code}"
    return URLResponse(short_code=db_url.short_code, short_url=short_url)


@app.get("/{short_code}", status_code=status.HTTP_307_TEMPORARY_REDIRECT, tags=["Redirects"])
def redirect_to_url(short_code: str, db: Session = Depends(get_db)) -> RedirectResponse:
    """Look up the short code and redirect to the original URL. Returns 404 if not found."""
    db_url = get_url_by_short_code(db=db, short_code=short_code)
    if db_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found",
        )
    return RedirectResponse(url=db_url.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
