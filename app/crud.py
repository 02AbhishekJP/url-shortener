"""CRUD operations for URL records."""

import secrets
import string

from sqlalchemy.orm import Session

from app.models import URL
from app.schemas import URLCreate

CHARSET = string.ascii_letters + string.digits
SHORT_CODE_LENGTH = 6


def generate_short_code(length: int = SHORT_CODE_LENGTH) -> str:
    """Generate a cryptographically random alphanumeric short code."""
    return "".join(secrets.choice(CHARSET) for _ in range(length))


def get_url_by_short_code(db: Session, short_code: str) -> URL | None:
    """Fetch a URL record by its short code, or None if not found."""
    return db.query(URL).filter(URL.short_code == short_code).first()


def create_short_url(db: Session, url: URLCreate) -> URL:
    """Generate a unique short code, persist the URL mapping, and return it."""
    # Retry until we get a code that doesn't collide with an existing one
    while True:
        short_code = generate_short_code()
        if not get_url_by_short_code(db, short_code):
            break

    db_url = URL(original_url=str(url.url), short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
