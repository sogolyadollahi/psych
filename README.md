# Psych

Psych is a backend-focused application built with **FastAPI** and **PostgreSQL**.

I built it mainly to work on the parts of backend development that are easy to skip when building small projects: authentication, database structure, service/repository separation, rate limiting, testing, Docker, CI, and integrating AI-related functionality into an actual backend.

The project is still a work in progress, but the main backend structure is in place.

---

## What it does

Psych currently includes:

* User registration and login
* Password hashing and verification
* JWT-based authentication
* Protected user endpoints
* PostgreSQL database
* SQLAlchemy ORM
* Alembic migrations
* Rate limiting
* Automated tests
* Docker
* GitHub Actions CI
* AI-related functionality

The main idea was not to build a huge application. I wanted to build a backend where the different pieces actually have to work together.

---

## Tech Stack

**Backend**

* Python
* FastAPI
* Pydantic
* SQLAlchemy

**Database**

* PostgreSQL
* Alembic

**Authentication & Security**

* JWT
* Argon2 password hashing
* FastAPI security dependencies
* Rate limiting with SlowAPI

**Testing**

* Pytest

**Infrastructure**

* Docker
* GitHub Actions
* GitHub Container Registry

---

## Project Structure

```text
app/
├── api/
│   └── v1/
│       └── auth.py
│
├── core/
│   ├── security.py
│   └── rate_limiter.py
│
├── services/
│   └── auth_service.py
│
├── repositories/
│   └── ...
│
├── models/
│   └── ...
│
├── schemas/
│   └── ...
│
└── ai/
    └── ...
    
tests/
└── test_auth.py
```

The project is separated into API, service, repository, schema, model, and core layers.

I kept this separation because I didn't want the route handlers to contain all of the application logic.

---

# Authentication

Authentication is handled with JWT access tokens.

The basic flow is:

```text
Register
   ↓
Hash password
   ↓
Store user in PostgreSQL

Login
   ↓
Find user by email
   ↓
Verify password
   ↓
Create JWT
   ↓
Return access token

Authenticated request
   ↓
Extract Bearer token
   ↓
Decode JWT
   ↓
Get user ID from "sub"
   ↓
Load current user
   ↓
Continue request
```

Passwords are never stored directly.

The password is hashed using `PasswordHash.recommended()` and verified when the user logs in.

The JWT contains the user's ID as the `sub` claim and an expiration time.

Tokens are signed using the configured secret key and algorithm.

---

## Why JWT?

I used JWT because it fits the type of API I wanted to build and keeps authentication stateless on the server side.

There is no server-side session object that needs to be stored for every logged-in user.

This also gave me a chance to work with things like:

* token expiration
* token validation
* invalid tokens
* missing claims
* protected FastAPI dependencies

---

# API

Authentication endpoints currently include:

### Register

```http
POST /api/v1/auth/register
```

Creates a new user.

Duplicate emails return a conflict response instead of creating another account.

### Login

```http
POST /api/v1/auth/login
```

Checks the user's credentials and returns an access token.

### Current User

```http
GET /api/v1/auth/me
```

Requires a valid Bearer token and returns the authenticated user.

---

# Rate Limiting

Authentication endpoints are rate limited.

For example, registration and login are limited to:

```text
5 requests / minute
```

This is mainly there to prevent simple brute-force or abuse scenarios on authentication endpoints.

I used **SlowAPI** for this instead of implementing the limiter myself.

---

# Database

The project uses **PostgreSQL** with SQLAlchemy.

Database changes are handled through **Alembic migrations** rather than manually changing the database schema.

The general flow is:

```text
SQLAlchemy Models
        ↓
Alembic Migration
        ↓
PostgreSQL
```

This makes schema changes easier to track and reproduce across environments.

---

# Testing

The authentication system has automated tests covering things such as:

* Password hashing
* Password verification
* Token creation
* Token decoding
* Expired tokens
* Invalid tokens
* Tokens without the required subject

Example:

```text
pytest
```

The goal here was not just to test the happy path.

Authentication tends to fail in the edge cases, so I specifically tested invalid and expired tokens as well.

---

# Docker

Psych can be run using Docker.

The project also builds a Docker image through GitHub Actions and pushes it to **GitHub Container Registry**.

This means the CI pipeline can verify the project and produce a container image without requiring a local Docker build.

---

# CI

GitHub Actions currently handles the main CI flow.

The pipeline:

1. Starts PostgreSQL
2. Sets up Python
3. Installs dependencies
4. Runs database migrations
5. Runs the test suite
6. Builds the Docker image
7. Pushes the image to GHCR

So a push to the repository is not just a code upload. The project is tested and built automatically.

---

# AI

Psych also contains an AI-related part of the application.

The idea is to keep AI functionality behind the backend rather than putting provider-specific logic directly into API routes.

This makes it possible to change or add providers without making the rest of the application depend directly on one implementation.

The AI side is still an area I plan to expand.

---

# What I learned building this

The biggest thing I got from this project wasn't FastAPI itself.

It was learning how the different parts of a backend fit together.

For example:

* A route shouldn't need to know how a password is hashed.
* Authentication logic shouldn't be duplicated across endpoints.
* Database access shouldn't be mixed with HTTP logic.
* Tests should cover failure cases, not just successful requests.
* Docker and CI should work with the project rather than being added at the very end.

I also got more comfortable debugging problems that only show up when multiple parts of the system interact.

---

# Things I would improve

Psych is not finished, and there are still things I want to improve.

Some of the next things on my list are:

* Expand the AI functionality
* Add more endpoint coverage
* Increase test coverage
* Improve error handling
* Add more production-oriented observability
* Improve deployment configuration
* Add more integration tests
* Continue tightening the authentication and security layer

---

# Running Locally

Clone the repository:

```bash
git clone https://github.com/sogolyadollahi/psych.git
cd psych
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your environment variables based on the project's configuration.

Run the migrations:

```bash
alembic upgrade head
```

Start the application:

```bash
uvicorn app.main:app --reload
```

The API documentation is then available through FastAPI's Swagger UI.

---

# Project Status

**Active development**

The core backend architecture is working, but Psych is still a project I'm actively improving rather than something I consider finished.

The repository is mainly a representation of how I approach backend development and the technologies I'm currently working with.

---

## Author

**Sogol Yadollahi**

Backend Developer focused on Python, FastAPI, APIs, automation, and backend systems.

GitHub: [sogolyadollahi](https://github.com/sogolyadollahi)
