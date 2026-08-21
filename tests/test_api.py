"""Tests for the URL Shortener API using an in-memory SQLite database."""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# In-memory SQLite for test isolation (no PostgreSQL required)
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_shorten_valid_url():
    response = client.post("/shorten", json={"url": "https://www.example.com/some/long/path"})
    assert response.status_code == 201

    data = response.json()
    assert "short_code" in data
    assert "short_url" in data
    assert len(data["short_code"]) == 6
    assert data["short_url"].endswith(data["short_code"])


def test_shorten_invalid_url():
    response = client.post("/shorten", json={"url": "not-a-valid-url"})
    assert response.status_code == 422


def test_redirect_existing_short_code():
    create_response = client.post("/shorten", json={"url": "https://www.google.com"})
    assert create_response.status_code == 201
    short_code = create_response.json()["short_code"]

    redirect_response = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"].startswith("https://www.google.com")


def test_redirect_nonexistent_short_code():
    response = client.get("/invalidCode")
    assert response.status_code == 404
    assert response.json()["detail"] == "Short URL not found"
