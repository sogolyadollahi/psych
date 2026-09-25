# Psych API

Psych is a fitness and nutrition tracking backend built with **FastAPI**.
It provides a REST API for managing workouts, meals, supplements, progress records, food scanning, nutrition data, user profiles, dashboards, and statistics.

The project is structured as a modular backend with separate API, service, repository, model, schema, and infrastructure layers.

---

## Features

### Authentication & Security

* User registration and login
* JWT-based authentication
* Password hashing with Argon2
* Protected API endpoints
* Current-user authentication dependency
* Password change
* Account deletion
* Request rate limiting
* Centralized HTTP and validation error handling

### User Profile

* Retrieve authenticated user profile
* Update profile information
* Personal information and fitness-related profile fields
* Password management
* Account deletion

### Workouts

* Create workouts
* List user workouts
* Retrieve individual workouts
* Update workouts
* Delete workouts
* User ownership protection

### Meals & Nutrition

* Create and manage meals
* Add, update, and delete meal items
* Search foods
* Retrieve nutritional information
* User ownership protection

### Supplements

* Create supplements
* List supplements
* Retrieve individual supplements
* Update supplements
* Delete supplements
* Supplement reminder infrastructure

### Progress Tracking

* Create progress records
* List progress records
* Retrieve individual records
* Update progress records
* Delete progress records
* Progress analytics
* Date-range filtering

### Food Scanner

* Image upload validation
* JPEG, PNG, and WEBP support
* Image size validation
* Corrupted-image detection
* Food recognition service
* Food candidate lookup
* Creation of meal items from scanned food

### Dashboard & Statistics

* Daily dashboard
* Dashboard summaries
* Fitness statistics
* Nutrition statistics
* Date-range based statistics

### Reliability

* Database transaction handling
* Centralized exception handling
* Application logging
* Background scheduler lifecycle
* API rate limiting
* Automated test suite

---

## Architecture

Psych follows a layered backend architecture:

```text
Client
  │
  ▼
FastAPI Router
  │
  ▼
Service Layer
  │
  ▼
Repository Layer
  │
  ▼
SQLAlchemy Models
  │
  ▼
PostgreSQL Database
```

Supporting components such as authentication, configuration, logging, scheduling, rate limiting, food recognition, and nutrition providers are organized under dedicated modules.

### Main Layers

#### API Layer

Located in:

```text
app/api/v1/
```

Responsible for:

* HTTP endpoints
* Request handling
* Authentication dependencies
* Response models
* API-level validation and documentation

#### Service Layer

Located in:

```text
app/services/
```

Responsible for:

* Business logic
* Authentication operations
* Workout management
* Meal management
* Supplement management
* Progress management
* Dashboard calculations
* Statistics
* Notifications
* Food scanning
* Nutrition services

#### Repository Layer

Located in:

```text
app/repositories/
```

Responsible for database access and persistence operations.

#### Models

Located in:

```text
app/models/
```

Contains SQLAlchemy database models.

#### Schemas

Located in:

```text
app/schemas/
```

Contains Pydantic request and response schemas.

#### Core

Located in:

```text
app/core/
```

Contains application infrastructure such as:

* Configuration
* Database setup
* Security
* Exception handling
* Logging
* Rate limiting
* Scheduler

---

## Project Structure

```text
psych/
│
├── app/
│   ├── ai/
│   │   └── food_recognition.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── dashboard.py
│   │       ├── deps.py
│   │       ├── food_scanner.py
│   │       ├── meals.py
│   │       ├── progress.py
│   │       ├── statistics.py
│   │       ├── supplement.py
│   │       ├── users.py
│   │       └── workout.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exception_handlers.py
│   │   ├── logging_config.py
│   │   ├── rate_limiter.py
│   │   ├── scheduler.py
│   │   └── security.py
│   │
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   │   ├── food_scanner/
│   │   └── nutrition/
│   ├── notifications/
│   └── utils/
│
├── migrations/
│   └── versions/
│
├── tests/
│
├── uploads/
│   ├── meals/
│   └── progress/
│
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Tech Stack

| Component        | Technology        |
| ---------------- | ----------------- |
| API Framework    | FastAPI           |
| ASGI Server      | Uvicorn           |
| ORM              | SQLAlchemy        |
| Database         | PostgreSQL        |
| Database Driver  | psycopg           |
| Migrations       | Alembic           |
| Validation       | Pydantic          |
| Configuration    | Pydantic Settings |
| Authentication   | JWT               |
| Password Hashing | Argon2 via pwdlib |
| Image Processing | Pillow            |
| Rate Limiting    | SlowAPI           |
| Scheduling       | APScheduler       |
| Testing          | Pytest            |
| HTTP Client      | HTTPX             |
| File Uploads     | python-multipart  |

---

## Requirements

Before running the project, make sure the following are available:

* Python
* PostgreSQL
* Git

A virtual environment is recommended.

---

## Installation

Clone the project and enter the project directory:

```bash
git clone <repository-url>
cd psych
```

Create and activate a virtual environment.

### Windows / PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

Use `.env.example` as the template:

```bash
cp .env.example .env
```

On Windows PowerShell, you can also copy it with:

```powershell
Copy-Item .env.example .env
```

Configure the environment values required by the application, including the database connection and application security settings.

**Do not commit `.env` to version control.**

---

## Database

Psych uses PostgreSQL with SQLAlchemy.

After configuring the database connection, apply the Alembic migrations:

```bash
alembic upgrade head
```

To check the current migration revision:

```bash
alembic current
```

---

## Running the API

Start the development server with:

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

### OpenAPI Schema

```text
http://127.0.0.1:8000/openapi.json
```

---

## API Overview

All versioned API endpoints use the following base path:

```text
/api/v1
```

### Authentication

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

### Workouts

```text
POST   /api/v1/workouts
GET    /api/v1/workouts
GET    /api/v1/workouts/{workout_id}
PATCH  /api/v1/workouts/{workout_id}
DELETE /api/v1/workouts/{workout_id}
```

### Meals

```text
POST   /api/v1/meals
GET    /api/v1/meals
GET    /api/v1/meals/{meal_id}
PATCH  /api/v1/meals/{meal_id}
DELETE /api/v1/meals/{meal_id}

POST   /api/v1/meals/{meal_id}/items
PATCH  /api/v1/meals/{meal_id}/items/{item_id}
DELETE /api/v1/meals/{meal_id}/items/{item_id}
```

### Food & Nutrition

```text
GET  /api/v1/meals/foods/search
POST /api/v1/meals/foods/nutrition
```

### Supplements

```text
POST   /api/v1/supplements
GET    /api/v1/supplements
GET    /api/v1/supplements/{supplement_id}
PATCH  /api/v1/supplements/{supplement_id}
DELETE /api/v1/supplements/{supplement_id}
```

### Food Scanner

```text
POST /api/v1/food-scanner/scan
GET  /api/v1/food-scanner/candidates
POST /api/v1/food-scanner/items
```

### Progress

```text
POST   /api/v1/progress
GET    /api/v1/progress
GET    /api/v1/progress/{progress_id}
PATCH  /api/v1/progress/{progress_id}
DELETE /api/v1/progress/{progress_id}

GET /api/v1/progress/analytics
```

### Dashboard

```text
GET /api/v1/dashboard/today
GET /api/v1/dashboard/summary
```

### Statistics

```text
GET /api/v1/statistics
```

### Users

```text
GET    /api/v1/users/me
PATCH  /api/v1/users/me
PATCH  /api/v1/users/me/password
DELETE /api/v1/users/me
```

### Health

```text
GET /health
```

---

## Testing

Run the complete test suite with:

```bash
pytest -v
```

The project contains tests covering authentication, services, APIs, security-related behavior, nutrition, food recognition, reminders, transactions, dashboard functionality, statistics, supplements, progress, and user services.

---

## Database Migrations

Create a new migration after model changes:

```bash
alembic revision --autogenerate -m "describe your change"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback one migration:

```bash
alembic downgrade -1
```

---

## Docker

The project includes:

```text
Dockerfile
docker-compose.yml
```

Docker configuration can be used to package and run the backend and its supporting infrastructure.

---

## Security

The application includes several security mechanisms:

* JWT authentication
* Argon2 password hashing
* Protected authenticated endpoints
* User ownership checks
* Request validation
* Image validation
* Rate limiting
* Centralized error handling
* Environment-based configuration

Sensitive configuration should remain outside source control.

---

## Development

Recommended development workflow:

```text
1. Update models / schemas
2. Create an Alembic migration
3. Implement repository operations
4. Implement service-layer business logic
5. Expose or update API endpoints
6. Add or update tests
7. Run pytest
8. Verify Swagger / ReDoc
```

---

## License

See the `LICENSE` file included in the project repository.
