# URL Shortener API

## 1. Project Title
URL Shortener REST API

## 2. Project Overview
A production-ready, lightweight URL shortening service built with FastAPI and PostgreSQL. It allows users to convert long URLs into easily shareable short links and automatically redirects users who visit those short links back to the original destination.

## 3. Problem Statement
Sharing long, complex URLs can be cumbersome in environments with character limits or when aiming for clean aesthetics. This API solves this by generating unique, shortened aliases for any valid web address.

## 4. Features
- Create short URLs from long valid URLs.
- Securely handles potential collisions during short code generation.
- Validates URLs prior to processing to maintain data integrity.
- Redirects short URLs to original URLs efficiently (HTTP 307).
- Persistent data storage using PostgreSQL.
- Dockerized setup for immediate execution.
- Comprehensive automated testing.

## 5. Technology Stack
- **Language**: Python 3.11+
- **Framework**: FastAPI (with Uvicorn as ASGI server)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.x
- **Data Validation**: Pydantic
- **Testing**: Pytest & HTTPX
- **Containerization**: Docker & Docker Compose

## 6. Project Architecture
The application follows a standard layered architecture for clear separation of concerns:
- **Routing Layer (`main.py`)**: Defines API endpoints and handles HTTP requests/responses.
- **Business Logic Layer (`crud.py`)**: Contains core application logic, including short code generation and database transactions.
- **Data Access Layer (`database.py`, `models.py`)**: Manages the SQLAlchemy ORM models and PostgreSQL database sessions.
- **Configuration Layer (`config.py`)**: Leverages `pydantic-settings` to manage environment variables safely.

## 7. Project Folder Structure
```text
url-shortener/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 8. Database Schema
Table name: `urls`

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key | Unique identifier for the record. |
| `original_url` | Text | Not Null | The original long URL submitted by the user. |
| `short_code` | Varchar | Unique, Not Null, Indexed | The 6-character generated short alias. |
| `created_at` | Timestamp | Not Null | UTC Timestamp when the short link was generated. |

## 9. API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/shorten` | Submits a long URL and returns a generated short code and URL. |
| `GET` | `/{short_code}` | Redirects the client to the original URL associated with the short code. |

## 10. Example Requests

### Create a Short URL
```bash
curl -X 'POST' \
  'http://localhost:8000/shorten' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "https://fastapi.tiangolo.com/advanced/testing-database/"
}'
```

### Redirect using a Short URL
```bash
# Using curl to view the redirect headers (it will return a 307 response)
curl -I http://localhost:8000/aB72xK
```

## 11. Example Responses

### Success (`POST /shorten`)
```json
{
  "short_code": "aB72xK",
  "short_url": "http://localhost:8000/aB72xK"
}
```

## 12. Error Responses

### Invalid URL submitted (`POST /shorten`) - `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "type": "url_parsing",
      "loc": [
        "body",
        "url"
      ],
      "msg": "Input should be a valid URL, relative URL without a base",
      "input": "not-a-valid-url"
    }
  ]
}
```

### Short Code Not Found (`GET /{short_code}`) - `404 Not Found`
```json
{
  "detail": "Short URL not found"
}
```

## 13. Local Setup Instructions
If you prefer running outside of Docker:
1. Ensure Python 3.11+ is installed.
2. Clone/download the repository.
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Create an `.env` file based on `.env.example` (see Environment Variables).

## 14. PostgreSQL Setup
For local execution, you must have PostgreSQL running. 
Create a database named `url_shortener` (or name it whatever you prefer and update the `.env` file).
Alternatively, the provided Docker Compose file automatically spins up a PostgreSQL instance.

## 15. Environment Variables
Create a file named `.env` in the root directory (alongside `requirements.txt`).
Refer to `.env.example`:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/url_shortener
BASE_URL=http://localhost:8000
```
*Note: If running via Docker Compose, you do not need to create this manually as the compose file provides the necessary environment variables to the container.*

## 16. Docker Setup
Ensure you have Docker and Docker Compose installed on your system.
The `docker-compose.yml` configures two services:
- `db`: PostgreSQL 15 database.
- `api`: The FastAPI application.

## 17. How to Run the Application

### Using Docker Compose (Recommended)
From the root directory of the project, run:
```bash
docker compose up --build
```
The API will be available at `http://localhost:8000`.

### Running Locally (Without Docker)
After completing local setup and configuring your PostgreSQL connection in `.env`, run:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 18. Swagger Documentation URL
FastAPI automatically generates interactive API documentation. Once the application is running, navigate to:
**http://localhost:8000/docs**

## 19. How to Run Tests
The tests use an in-memory SQLite database (`sqlite:///:memory:`) so they are isolated and do not require PostgreSQL to be running.
From the root project directory, execute:
```bash
pytest
```
To run tests with output:
```bash
pytest -v
```

## 20. Design Decisions and Assumptions
- **Testing Strategy**: Tests utilize FastAPI's `TestClient` combined with dependency injection overrides. Specifically, the `get_db` dependency is overridden to yield a session connected to an in-memory SQLite database, completely isolating tests from the production PostgreSQL environment.
- **Short Code Algorithm**: Generated securely via `secrets.choice` selecting from 62 characters (A-Z, a-z, 0-9). While generating 6 random characters presents a low collision rate initially (62^6 possibilities), a `while` loop checks the database to prevent duplicate collisions before inserting.
- **Redirects**: A `307 Temporary Redirect` is used instead of a `301 Permanent Redirect`. This ensures that analytics could theoretically be tracked on every click if added in the future, as the browser won't permanently cache the redirect.
- **Security**: The application relies on Pydantic's `HttpUrl` for strong initial URL validation, preventing arbitrary inputs and ensuring data sanitation prior to persistence.
