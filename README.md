# URL Shortener API

A production-ready URL shortening service built with **FastAPI** and **PostgreSQL**. Convert long URLs into short, shareable links with instant redirects.

## Features

- **Shorten URLs** — Submit any valid URL and get a unique 6-character short code.
- **Instant Redirects** — Visit a short link and get redirected (HTTP 307) to the original URL.
- **Collision-Safe** — Cryptographically random codes with automatic retry on collision.
- **URL Validation** — Pydantic-powered input validation rejects malformed URLs.
- **Persistent Storage** — PostgreSQL-backed for reliable data persistence.
- **Dockerized** — Full Docker Compose setup for local development.
- **Tested** — Automated test suite using in-memory SQLite (no DB setup needed).

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Framework | FastAPI + Uvicorn |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.x |
| Validation | Pydantic v2 |
| Testing | Pytest + HTTPX |
| Deployment | Netlify |

## Project Structure

```
url-shortener/
├── app/
│   ├── __init__.py      # Package marker
│   ├── main.py          # API endpoints & app factory
│   ├── database.py      # Engine, session, Base class
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── crud.py          # Business logic & DB operations
│   └── config.py        # Environment-based settings
├── tests/
│   ├── __init__.py
│   └── test_api.py      # API integration tests
├── .env.example         # Sample environment variables
├── .gitignore
├── netlify/             # Netlify Functions
├── netlify.toml         # Netlify configuration
├── requirements.txt     # Python dependencies
└── README.md
```

## Database Schema

**Table: `urls`**

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Auto-increment identifier |
| `original_url` | Text | Not Null | The original long URL |
| `short_code` | Varchar(6) | Unique, Indexed, Not Null | Generated short alias |
| `created_at` | Timestamp | Not Null | UTC creation timestamp |

## API Endpoints

### `POST /shorten`

Create a shortened URL.

**Request:**
```json
{
  "url": "https://fastapi.tiangolo.com/advanced/testing-database/"
}
```

**Response (201 Created):**
```json
{
  "short_code": "aB72xK",
  "short_url": "https://your-app.netlify.app/aB72xK"
}
```

### `GET /{short_code}`

Redirects to the original URL (HTTP 307).

```bash
curl -I https://your-app.netlify.app/aB72xK
```

### Error Responses

| Status | Condition | Body |
|---|---|---|
| `422` | Invalid URL submitted | Pydantic validation error details |
| `404` | Short code not found | `{"detail": "Short URL not found"}` |

## Local Development

### Option 1: Docker Compose (Recommended)

```bash
docker compose up --build
```

API available at `http://localhost:8000`

### Option 2: Manual Setup

1. Install Python 3.11+
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and configure your PostgreSQL connection.
5. Run the server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Interactive Docs

Once running, visit **http://localhost:8000/docs** for Swagger UI.

## Running Tests

Tests use an in-memory SQLite database — no PostgreSQL required.

```bash
pytest -v
```

## Deploy to Render (Recommended for FastAPI + PostgreSQL)

### 1-Click Blueprint Setup

1. Push this repository to GitHub.
2. Log into [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** -> **Blueprint**.
4. Connect your GitHub repository (`url-shortener`).
5. Render auto-detects `render.yaml` and provisions both your **FastAPI Web Service** and **PostgreSQL Database** automatically!
6. Click **Apply**! 🚀

## Deploy to Netlify

1. Push this repository to GitHub.
2. Go to [Netlify Dashboard](https://app.netlify.com) and click **Add new site** -> **Import an existing project**.
3. Select GitHub and connect your repository (`url-shortener`).
4. Netlify will auto-detect `netlify.toml` and configure build settings.
5. Under **Environment variables**, set `DATABASE_URL` (e.g. Supabase, Neon, etc.).
6. Click **Deploy site**! 🚀

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost:5432/url_shortener` |
| `BASE_URL` | Public URL for generating short links | Auto-detected on Render (`RENDER_EXTERNAL_URL`) & Netlify (`URL`), `http://localhost:8000` locally |

## Design Decisions

- **307 Temporary Redirect** — Allows future analytics tracking (browsers won't cache the redirect permanently).
- **`secrets.choice`** — Cryptographically secure random code generation (62^6 = 56.8 billion possibilities).
- **Pydantic `HttpUrl`** — Strong URL validation before persistence, preventing injection of arbitrary strings.
- **Render / Netlify Ready** — Deployable via Render Blueprint (`render.yaml`) or Netlify Functions (`netlify.toml`).

