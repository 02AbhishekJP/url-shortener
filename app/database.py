"""Database engine, session factory, and request-scoped dependency."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

db_url = settings.database_url
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

connect_args = {}
if db_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

try:
    engine = create_engine(db_url, connect_args=connect_args)
except Exception as e:
    print(f"Failed to create engine with {db_url}: {e}")
    engine = create_engine("sqlite:////tmp/url_shortener.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed after the request."""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"DB creation warning: {e}")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
