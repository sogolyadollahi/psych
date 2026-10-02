# Psych

Psych is a backend-focused fitness and nutrition API built with **Python, FastAPI, and PostgreSQL**.

The project was built to practice and demonstrate real backend concerns beyond basic CRUD: authentication, authorization, database design, service/repository separation, validation, transactions, rate limiting, external API integration, AI integration, testing, Docker, and CI/CD.

## Project Status

**Backend v1.0 — feature complete and in final portfolio cleanup.**

The core backend has been implemented and audited. The repository is intentionally kept backend-only; there is no frontend and no paid deployment requirement.

The current CI pipeline verifies migrations, the automated test suite, and Docker image creation on pushes to `master`.

## Main Features

- User registration and login
- JWT-based authentication
- Argon2 password hashing
- Protected endpoints and ownership checks
- User profiles
- Workout management
- Meal and nutrition tracking
- Supplement management
- Reminders and scheduled tasks
- Progress tracking
- Dashboard and statistics
- Food scanning / AI-assisted food detection
- USDA FoodData Central integration
- Request rate limiting
- Input validation with Pydantic
- Transaction-safe database operations
- Structured API error responses
- Configurable external-service timeouts
- Centralized application logging
- Automated tests
- Docker support
- GitHub Actions CI
- GitHub Container Registry image publishing

## Architecture

Psych follows a layered backend structure so that HTTP handling, business logic, persistence, and infrastructure concerns are not tightly coupled.

```text
Client
  |
  v
FastAPI API Routes
  |
  v
Services
  |
  v
Repositories
  |
  v
SQLAlchemy ORM
  |
  v
PostgreSQL
```

Cross-cutting concerns such as authentication, configuration, rate limiting, logging, scheduling, and exception handling live under `app/core/`.

AI and external-data integrations are kept behind dedicated components instead of placing provider-specific logic directly inside route handlers.

## Project Structure

```text
app/
├── api/
│   └── v1/
│       ├── auth.py
│       ├── dashboard.py
│       ├── food_scanner.py
│       ├── meals.py
│       ├── progress.py
│       ├── statistics.py
│       ├── supplement.py
│       ├── users.py
│       └── workout.py
│
├── core/
│   ├── config.py
│   ├── database.py
│   ├── exception_handlers.py
│   ├── logging_config.py
│   ├── rate_limiter.py
│   ├── scheduler.py
│   └── security.py
│
├── models/
├── schemas/
├── repositories/
├── services/
├── notifications/
├── ai/
└── main.py

alembic/
tests/
Dockerfile
docker-compose.yml
.github/
└── workflows/
```

The exact contents of individual packages may evolve, but the main architectural boundaries are intentionally kept clear.

## Authentication & Security

Authentication uses JWT access tokens.

The basic flow is:

```text
Register
   ↓
Validate input
   ↓
Hash password
   ↓
Store user

Login
   ↓
Find user
   ↓
Verify password
   ↓
Create JWT
   ↓
Return access token

Authenticated request
   ↓
Validate Bearer token
   ↓
Read user ID from "sub"
   ↓
Load current user
   ↓
Apply authorization / ownership checks
   ↓
Execute endpoint
```

Passwords are never stored directly. Password hashing uses `pwdlib.PasswordHash.recommended()`.

JWTs contain the user ID in the `sub` claim and an expiration time. The signing secret, algorithm, and token lifetime are configurable through environment variables.

Authentication endpoints are rate limited to reduce simple brute-force and abuse scenarios.

The application also includes validation and error handling around external integrations, file uploads, database operations, and protected resources.

## Database

Psych uses:

- **PostgreSQL**
- **SQLAlchemy**
- **Alembic**

Database changes are represented as migrations rather than manual schema changes.

The request-level database dependency commits successful transactions, rolls back failed transactions, and closes the session.

Foreign-key relationships use cascading behavior where appropriate so user-owned data does not become orphaned.

## API Areas

The API is organized under `/api/v1/`.

| Area | Purpose |
|---|---|
| Auth | Registration, login, current-user authentication |
| Users | User/profile operations |
| Workouts | Workout data and tracking |
| Meals | Meals, food items, nutrition, USDA integration |
| Supplements | Supplement records and management |
| Progress | Body measurements and progress tracking |
| Dashboard | Aggregated user dashboard data |
| Statistics | Date-based statistics and summaries |
| Food Scanner | Image-based food detection and candidates |

FastAPI automatically exposes interactive API documentation when documentation is enabled.

## Food Scanner & AI

The food-scanning subsystem separates the API layer from the food-detection implementation.

The project supports an Ollama-based detector and keeps provider-specific behavior behind dedicated detector classes.

The food scanner also validates uploaded images and maps failures from external AI and USDA services to appropriate API responses instead of exposing raw provider exceptions.

External service timeouts are configurable so a slow provider cannot hold a request indefinitely.

## Rate Limiting

Rate limiting is implemented with **SlowAPI**.

Sensitive and externally backed endpoints use request limits to reduce abuse and accidental overload.

Limits are applied at the API boundary rather than being mixed into business logic.

## Error Handling

Psych uses structured JSON responses for application errors.

The general error shape is:

```json
{
  "success": false,
  "error": {
    "code": "...",
    "message": "..."
  }
}
```

Unhandled exceptions are logged with their traceback while the API returns a generic 500 response instead of exposing internal implementation details.

External service failures are mapped to controlled API errors.

## Testing

The test suite covers multiple layers of the application, including:

- Authentication and password security
- JWT creation and validation
- Protected endpoint dependencies
- Dashboard behavior
- Meal and nutrition services
- Progress APIs and services
- Reminder and scheduler behavior
- Statistics
- Supplement APIs and services
- User services
- Workout functionality
- Food detection integrations
- Transaction behavior
- Database connectivity
- Security-related behavior

The CI pipeline runs the test suite against PostgreSQL rather than relying only on an isolated local environment.

## Docker

Psych includes:

- `Dockerfile`
- `docker-compose.yml`
- `.env.docker.example`
- `.dockerignore`

For local Docker usage, create a private `.env.docker` from `.env.docker.example` and provide your own secrets/API keys.

The application container exposes port `8000` internally and the provided Compose configuration maps it to port `9000` on the host.

PostgreSQL runs as a separate Compose service with a persistent named volume.

## CI/CD

GitHub Actions runs the main verification pipeline on pushes and pull requests.

The current pipeline:

1. Starts PostgreSQL
2. Checks out the repository
3. Sets up Python
4. Installs dependencies
5. Runs Alembic migrations
6. Runs the full pytest suite
7. Logs into GitHub Container Registry
8. Builds the Docker image
9. Pushes the image to GHCR

The latest cleanup pipeline was verified successfully, including:

- dependency installation
- database migrations
- automated tests
- Docker metadata generation
- Docker image build
- Docker image push

## Configuration

Secrets and environment-specific configuration are not committed to the repository.

Use the example environment file as a starting point:

```text
.env.docker.example
```

Important values include:

- `DATABASE_URL`
- `SECRET_KEY`
- `USDA_API_KEY`
- `GEMINI_API_KEY`
- `AI_PROVIDER`
- `AI_MODEL`
- external-service timeout settings
- CORS configuration

Never commit real API keys or production secrets.

## Running Locally

Clone the repository:

```bash
git clone https://github.com/sogolyadollahi/psych.git
cd psych
```

Create and activate a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\\Scripts\\activate
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` containing the required configuration values.

Run migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn app.main:app --reload
```

### Docker Compose

For Docker-based local development:

```bash
cp .env.docker.example .env.docker
```

Fill in the required secrets, then run:

```bash
docker compose up --build
```

The API will be available on:

```text
http://localhost:9000
```

## What This Project Demonstrates

Psych was designed as a practical backend project rather than a collection of disconnected endpoints.

The main engineering goals were:

- Keep route handlers thin.
- Separate business logic from persistence.
- Make authentication reusable through dependencies.
- Enforce ownership at the service/API boundary.
- Treat database transactions as a first-class concern.
- Validate external input before processing it.
- Handle third-party failures explicitly.
- Test failure paths as well as happy paths.
- Make the project reproducible with migrations and Docker.
- Automate verification through CI.

## Project Scope

The project intentionally does **not** include:

- A frontend application
- A paid production server
- A managed database
- Unnecessary background infrastructure such as Redis/Celery

The goal is a focused backend portfolio project with enough real-world engineering concerns to demonstrate practical Python backend development.

## Author

**Sogol Yadollahi**

Backend Developer focused on Python, FastAPI, APIs, automation, and backend systems.

GitHub: https://github.com/sogolyadollahi
