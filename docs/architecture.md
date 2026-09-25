# Psych API — Architecture Documentation

## 1. Architecture Overview

Psych is a FastAPI-based backend for fitness and nutrition tracking.

The application follows a layered architecture that separates HTTP/API concerns from business logic, data access, database models, and infrastructure components.

The main request flow is:

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

The architecture is designed to keep responsibilities separated and make the application easier to maintain, test, and extend.

---

## 2. Project Layers

The main application structure is:

```text
app/
├── api/
│   └── v1/
├── services/
├── repositories/
├── models/
├── schemas/
├── core/
├── ai/
├── notifications/
└── utils/
```

Each layer has a specific responsibility.

### API Layer

Responsible for:

* HTTP endpoints
* Request handling
* Authentication dependencies
* Input/output schema binding
* HTTP status codes
* API documentation

Location:

```text
app/api/v1/
```

### Service Layer

Responsible for:

* Business logic
* Application workflows
* Coordinating repositories
* Validation beyond basic request validation
* Combining data from multiple sources when necessary

Location:

```text
app/services/
```

### Repository Layer

Responsible for:

* Database access
* Query construction
* CRUD operations
* Persistence-related logic

Location:

```text
app/repositories/
```

### Model Layer

Contains SQLAlchemy ORM models representing persistent database entities.

Location:

```text
app/models/
```

### Schema Layer

Contains Pydantic schemas used for:

* Request validation
* Response serialization
* Data transfer between API and application layers

Location:

```text
app/schemas/
```

### Core Layer

Contains shared application infrastructure such as:

* Configuration
* Database setup
* Security
* Logging
* Exception handling
* Rate limiting
* Scheduler configuration

Location:

```text
app/core/
```

---

## 3. Request Flow

A typical authenticated API request follows this flow:

```text
HTTP Request
     │
     ▼
FastAPI Router
     │
     ▼
Authentication / Dependencies
     │
     ▼
Pydantic Schema Validation
     │
     ▼
Service
     │
     ▼
Repository
     │
     ▼
SQLAlchemy
     │
     ▼
PostgreSQL
     │
     ▼
Repository
     │
     ▼
Service
     │
     ▼
Response Schema
     │
     ▼
HTTP Response
```

The router should primarily coordinate the request rather than contain complex business logic.

---

## 4. API / Router Layer

API routes are located under:

```text
app/api/v1/
```

Current API modules include:

```text
auth.py
dashboard.py
deps.py
food_scanner.py
meals.py
meal_deps.py
profile.py
progress.py
reminder.py
reminder_deps.py
statistics.py
supplement.py
supplement_deps.py
users.py
workout.py
```

The routers expose functionality through FastAPI endpoints.

Examples include:

```text
/api/v1/auth
/api/v1/workouts
/api/v1/meals
/api/v1/supplements
/api/v1/progress
/api/v1/dashboard
/api/v1/statistics
/api/v1/food-scanner
/api/v1/users
```

The API layer is also responsible for attaching the appropriate authentication dependencies and returning HTTP-level responses.

---

## 5. Service Layer

Business logic is implemented primarily in:

```text
app/services/
```

Examples include:

```text
auth_service.py
dashboard_service.py
meal_service.py
meal_item_service.py
progress_service.py
statistics_service.py
supplement_service.py
user_service.py
workout_service.py
```

The service layer acts as the main application/business layer.

For example:

```text
Workout Router
      │
      ▼
Workout Service
      │
      ▼
Workout Repository
      │
      ▼
Database
```

This separation prevents database operations and business rules from becoming tightly coupled to HTTP endpoint implementations.

---

## 6. Repository Layer

Repositories are located in:

```text
app/repositories/
```

Current repositories include:

```text
meal_repository.py
meal_item_repository.py
progress_repository.py
supplement_repository.py
user_repository.py
workout_repository.py
```

Repositories encapsulate database access.

Their responsibilities include operations such as:

* Creating records
* Retrieving records
* Updating records
* Deleting records
* Filtering records
* Querying user-owned resources

The repository layer allows services to work with application-level operations without placing raw database queries directly inside API routes.

---

## 7. Model Layer

SQLAlchemy models are located in:

```text
app/models/
```

Current models include:

```text
user.py
workout.py
meal.py
meal_item.py
supplement.py
progress.py
```

These models represent the application's persistent entities and their relationships.

The `User` model is the central ownership entity for user-specific data.

Relationships include:

```text
User
 ├── Workouts
 ├── Meals
 ├── Supplements
 └── Progress Records
```

User-owned relationships use cascading deletion where appropriate so that dependent records are handled together with their owning user.

---

## 8. Schema Layer

Pydantic schemas are located in:

```text
app/schemas/
```

Current schema modules include:

```text
dashboard.py
food_scanner.py
meal.py
progress.py
statistics.py
supplement.py
user.py
workout.py
```

Schemas define the external data contract of the API.

They are used to validate incoming requests and serialize outgoing responses.

For example:

```text
Client JSON
    │
    ▼
Pydantic Request Schema
    │
    ▼
Service
    │
    ▼
Database
    │
    ▼
Pydantic Response Schema
    │
    ▼
Client JSON
```

Keeping schemas separate from SQLAlchemy models prevents database implementation details from becoming the public API contract.

---

## 9. Core / Infrastructure

Shared infrastructure is located under:

```text
app/core/
```

Important modules include:

### Configuration

```text
config.py
```

Centralizes application configuration and environment-based settings.

### Database

```text
database.py
```

Provides SQLAlchemy database infrastructure and session management.

### Security

```text
security.py
```

Handles security-related functionality such as password hashing and JWT-based authentication.

### Exception Handling

```text
exception_handlers.py
```

Provides centralized handling for application exceptions and HTTP errors.

### Logging

```text
logging_config.py
```

Provides application logging configuration.

### Rate Limiting

```text
rate_limiter.py
```

Provides request rate limiting using SlowAPI.

### Scheduler

```text
scheduler.py
```

Provides application scheduling infrastructure used by reminder-related functionality.

---

## 10. Authentication and Security Flow

Authentication is based on JWT access tokens.

The general flow is:

```text
Register
   │
   ▼
Password Hashing
   │
   ▼
User Stored in Database
```

For login:

```text
Email + Password
       │
       ▼
Authenticate User
       │
       ▼
Verify Password Hash
       │
       ▼
Create JWT Access Token
       │
       ▼
Client
```

For protected endpoints:

```text
HTTP Request
     │
     ▼
Authorization Header
     │
     ▼
JWT Validation
     │
     ▼
Current User
     │
     ▼
Protected Endpoint
```

Passwords are stored as secure password hashes rather than plaintext passwords.

Protected resources are also checked against the authenticated user's ownership.

---

## 11. Food Scanner Architecture

Food scanning has its own internal service structure.

Relevant components are located under:

```text
app/services/food_scanner/
```

The scanner architecture includes:

```text
scanner_service.py
detector.py
gemini_detector.py
mock_detector.py
ollama_detector.py
openai_detector.py
image_validator.py
```

The general flow is:

```text
Uploaded Image
      │
      ▼
Image Validation
      │
      ▼
Scanner Service
      │
      ▼
Detection Provider
      │
      ├── OpenAI
      ├── Gemini
      ├── Ollama
      └── Mock Detector
      │
      ▼
Detection Result
```

This provider-oriented structure allows the detection implementation to be changed without moving the scanner's API responsibilities into the detector itself.

---

## 12. Nutrition Architecture

Nutrition-related functionality is located under:

```text
app/services/nutrition/
```

Current components include:

```text
nutrition_service.py
usda_provider.py
```

The nutrition service provides an application-level interface while the provider handles the external nutrition data source.

Conceptually:

```text
API
 │
 ▼
Meal Service
 │
 ▼
Nutrition Service
 │
 ▼
USDA Provider
 │
 ▼
Nutrition Data
```

This separation makes the nutrition provider replaceable without requiring changes throughout the API layer.

---

## 13. Notifications and Scheduler

Notification-related functionality is located under:

```text
app/notifications/
```

Current notification components include:

```text
base.py
log_provider.py
```

Application-level notification functionality is handled through:

```text
app/services/notification_service.py
```

Reminder functionality is implemented through:

```text
app/services/reminder_service.py
app/services/reminder_runner.py
app/services/scheduler.py
```

The architecture separates:

* Reminder business logic
* Scheduled execution
* Notification delivery

This allows notification providers to be extended independently from reminder scheduling.

---

## 14. Database and Migrations

Psych uses SQLAlchemy for ORM/database interaction and Alembic for schema migrations.

Migration files are located under:

```text
migrations/
└── versions/
```

The migration history includes changes for:

* Users
* Workouts
* Meals and meal items
* Supplements
* Progress
* User profile fields

The migration workflow is:

```text
SQLAlchemy Models
      │
      ▼
Alembic Migration
      │
      ▼
PostgreSQL Schema
```

Database schema changes should be represented through migrations rather than manually modifying the production database schema.

---

## 15. Transactions

Database transaction handling is centralized around the database session lifecycle.

A typical operation follows:

```text
Begin Transaction
      │
      ▼
Database Operations
      │
      ├── Success ──► Commit
      │
      └── Error ────► Rollback
```

Transaction handling is important for operations that modify multiple related records and ensures that partial database changes are not persisted when an operation fails.

---

## 16. Dashboard and Statistics

Dashboard functionality is implemented through:

```text
app/services/dashboard_service.py
```

Statistics functionality is implemented through:

```text
app/services/statistics_service.py
```

The architecture keeps aggregation and calculation logic inside the service layer rather than directly inside API routes.

Conceptually:

```text
Dashboard / Statistics API
          │
          ▼
      Service Layer
          │
          ▼
   Repository / Database
          │
          ▼
      Aggregated Data
```

---

## 17. Error Handling

Psych uses centralized exception handling through:

```text
app/core/exception_handlers.py
```

The goal is to keep error responses consistent across API endpoints.

The architecture separates:

```text
Application Error
      │
      ▼
Exception Handler
      │
      ▼
HTTP Error Response
```

This prevents every individual endpoint from having to implement identical error formatting.

---

## 18. Rate Limiting

Rate limiting is implemented through SlowAPI.

The limiter is configured in:

```text
app/core/rate_limiter.py
```

Selected sensitive endpoints have request limits, including authentication and food scanning endpoints.

The general flow is:

```text
Request
  │
  ▼
Rate Limiter
  │
  ├── Allowed ──► Endpoint
  │
  └── Exceeded ─► HTTP 429
```

Rate limiting provides an additional layer of protection against excessive requests and abuse.

---

## 19. Testing Architecture

Tests are located under:

```text
tests/
```

The test suite covers multiple application areas, including:

```text
Authentication
Database connectivity
Dashboard
Meals
Nutrition
Food detection
Progress
Reminders
Security
Statistics
Supplements
Users
Workouts
Transactions
```

The project uses `pytest` as its primary testing framework.

Tests can be executed with:

```powershell
pytest -v
```

The test suite provides regression protection as the application evolves.

---

## 20. Application Lifecycle

The FastAPI application is initialized in:

```text
app/main.py
```

The main application is responsible for:

* Creating the FastAPI application
* Registering API routers
* Configuring CORS
* Registering exception handlers
* Configuring rate limiting
* Managing application startup/shutdown lifecycle
* Starting and stopping scheduler-related infrastructure
* Exposing the health endpoint

The API documentation is available through:

```text
/docs
/redoc
/openapi.json
```

---

## 21. Complete Architecture Diagram

The complete high-level architecture can be represented as:

```text
                         ┌──────────────────┐
                         │      Client      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   FastAPI API    │
                         │     Routers      │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
             Authentication              Request Schemas
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Service Layer   │
                         │  Business Logic  │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
              Repositories      AI/Nutrition   Notifications
                    │             │             │
                    └─────────────┼─────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    SQLAlchemy    │
                         │      Models      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    PostgreSQL    │
                         └──────────────────┘
```

---

## 22. Design Principles

The current architecture follows several important principles:

### Separation of Concerns

Each layer has a defined responsibility.

### Dependency Isolation

Database access is separated from business logic through repositories.

### Business Logic Isolation

Business rules are primarily implemented in services rather than API routes.

### Schema Separation

Pydantic schemas are separated from SQLAlchemy persistence models.

### Provider Abstraction

External integrations such as food recognition and nutrition providers are isolated behind application-level services.

### Security by Layer

Authentication, ownership checks, password hashing, JWT validation, rate limiting, and centralized error handling are distributed across appropriate infrastructure and application layers.

### Testability

The layered structure allows individual services and components to be tested without requiring every test to go through the complete HTTP stack.

---

## 23. Example: Creating a Workout

A simplified workout creation request follows this path:

```text
POST /api/v1/workouts
          │
          ▼
Workout Router
          │
          ▼
Authentication Dependency
          │
          ▼
Workout Request Schema
          │
          ▼
Workout Service
          │
          ▼
Workout Repository
          │
          ▼
SQLAlchemy Workout Model
          │
          ▼
PostgreSQL
          │
          ▼
Workout Response Schema
          │
          ▼
HTTP 201 Response
```

Each layer performs only the responsibilities appropriate to it.

---

## 24. Summary

Psych is structured as a layered FastAPI application:

```text
API
 ↓
Services
 ↓
Repositories
 ↓
Models
 ↓
Database
```

Supporting infrastructure provides:

```text
Authentication
Security
Configuration
Logging
Exception Handling
Rate Limiting
Scheduling
AI Providers
Nutrition Providers
Notifications
Testing
```

This structure provides a clear separation between HTTP handling, business logic, persistence, and infrastructure, making the project easier to maintain and extend as new features are added.
