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

## Deploy to Render

### Option 1: Blueprint (Recommended - 1-Click Setup)

1. Push this repository to GitHub.
2. Log into [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** -> **Blueprint**.
4. Connect your GitHub repository. Render will automatically detect `render.yaml` and provision both:
   - **PostgreSQL Database** (`url-shortener-db`)
   - **FastAPI Web Service** (`url-shortener-api`)
5. Click **Apply**. Render will automatically build the service, spin up PostgreSQL, link `DATABASE_URL`, and auto-detect `RENDER_EXTERNAL_URL`.

### Option 2: Manual Setup on Render

1. **Database**: Create a new **PostgreSQL** database on Render, copy its **Internal Database URL**.
2. **Web Service**: Create a new **Web Service** on Render connected to this repository:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     - `DATABASE_URL`: Set to your Render PostgreSQL connection string.

## Deploy to Netlify

1. Push this repo to GitHub.
2. Go to [netlify.com](https://netlify.com) and create a new site from GitHub.
3. Netlify auto-detects `netlify.toml` and configures function routing.
4. Set required environment variables (e.g. `DATABASE_URL`) in Netlify Site Configuration.
5. Deploy! 🚀

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

