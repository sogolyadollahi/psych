# Psych API — Demo Guide

## 1. Overview

This document provides a practical demonstration flow for the Psych API.

The demo follows a typical user journey:

```text
Health Check
     ↓
Register
     ↓
Login
     ↓
Authenticated Requests
     ↓
Workout
     ↓
Meal
     ↓
Supplement
     ↓
Progress
     ↓
Dashboard
     ↓
Statistics
     ↓
Food Scanner
     ↓
User Account Management
```

The API base path is:

```text
/api/v1
```

The interactive API documentation is available at:

```text
/docs
```

---

# 2. Health Check

The health endpoint is available outside the versioned API.

### Endpoint

```http
GET /health
```

### Expected response

```json
{
  "status": "OK"
}
```

This endpoint can be used as a basic application availability check.

---

# 3. Authentication

## 3.1 Register

Create a new user account.

### Endpoint

```http
POST /api/v1/auth/register
```

The request body is defined by the authentication request schema.

Example structure:

```json
{
  "email": "demo@example.com",
  "password": "StrongPassword123"
}
```

A successful registration creates the user account.

Possible documented responses include:

* `201` — User created
* `409` — Email is already registered
* `422` — Validation error

---

## 3.2 Login

Authenticate the user and receive an access token.

### Endpoint

```http
POST /api/v1/auth/login
```

Example:

```json
{
  "username": "demo@example.com",
  "password": "StrongPassword123"
}
```

A successful login returns an access token.

The token is then used for authenticated endpoints.

---

## 3.3 Authentication Header

Authenticated requests use:

```http
Authorization: Bearer <ACCESS_TOKEN>
```

The JWT is validated before protected resources are accessed.

---

## 3.4 Current User

Retrieve the currently authenticated user.

### Endpoint

```http
GET /api/v1/auth/me
```

This endpoint requires authentication.

---

# 4. Workouts

Workout endpoints are available under:

```text
/api/v1/workouts
```

## Create Workout

```http
POST /api/v1/workouts
```

Requires authentication.

## List Workouts

```http
GET /api/v1/workouts
```

Returns the authenticated user's workouts.

## Get Workout

```http
GET /api/v1/workouts/{workout_id}
```

## Update Workout

```http
PATCH /api/v1/workouts/{workout_id}
```

## Delete Workout

```http
DELETE /api/v1/workouts/{workout_id}
```

Workout resources are associated with the authenticated user.

---

# 5. Meals

Meal functionality is available under:

```text
/api/v1/meals
```

## Create Meal

```http
POST /api/v1/meals
```

## List Meals

```http
GET /api/v1/meals
```

## Get Meal

```http
GET /api/v1/meals/{meal_id}
```

## Update Meal

```http
PATCH /api/v1/meals/{meal_id}
```

## Delete Meal

```http
DELETE /api/v1/meals/{meal_id}
```

---

## 5.1 Meal Items

Meal items are managed through the meal resource.

### Add Item

```http
POST /api/v1/meals/{meal_id}/items
```

### Update Item

```http
PATCH /api/v1/meals/{meal_id}/items/{item_id}
```

### Delete Item

```http
DELETE /api/v1/meals/{meal_id}/items/{item_id}
```

---

## 5.2 Food Search

Search for food information.

```http
GET /api/v1/meals/foods/search
```

---

## 5.3 Nutrition Lookup

Retrieve nutrition information for a food.

```http
POST /api/v1/meals/foods/nutrition
```

---

# 6. Supplements

Supplement functionality is available under:

```text
/api/v1/supplements
```

## Create Supplement

```http
POST /api/v1/supplements
```

## List Supplements

```http
GET /api/v1/supplements
```

## Get Supplement

```http
GET /api/v1/supplements/{supplement_id}
```

## Update Supplement

```http
PATCH /api/v1/supplements/{supplement_id}
```

## Delete Supplement

```http
DELETE /api/v1/supplements/{supplement_id}
```

Supplement resources belong to the authenticated user.

---

# 7. Progress Tracking

Progress endpoints are available under:

```text
/api/v1/progress
```

## Create Progress Record

```http
POST /api/v1/progress
```

## List Progress Records

```http
GET /api/v1/progress
```

## Get Progress Record

```http
GET /api/v1/progress/{progress_id}
```

## Update Progress Record

```http
PATCH /api/v1/progress/{progress_id}
```

## Delete Progress Record

```http
DELETE /api/v1/progress/{progress_id}
```

---

## 7.1 Progress Analytics

Retrieve progress analytics.

```http
GET /api/v1/progress/analytics
```

This endpoint requires authentication.

---

# 8. Dashboard

Dashboard functionality is available under:

```text
/api/v1/dashboard
```

## Today's Dashboard

```http
GET /api/v1/dashboard/today
```

Returns the current dashboard data for the authenticated user.

## Dashboard Summary

```http
GET /api/v1/dashboard/summary
```

Returns a dashboard summary for the requested context.

---

# 9. Statistics

Statistics are available through:

```http
GET /api/v1/statistics
```

This endpoint requires authentication and provides fitness/nutrition statistics for the user.

---

# 10. Food Scanner

Food scanning functionality is available under:

```text
/api/v1/food-scanner
```

## 10.1 Scan Food Image

```http
POST /api/v1/food-scanner/scan
```

This endpoint accepts an uploaded food image.

The scanner validates the uploaded file before passing it to the configured detection provider.

Possible documented errors include:

* `400` — Invalid request
* `401` — Authentication error
* `413` — Uploaded file is too large
* `422` — Validation error
* `429` — Rate limit exceeded

---

## 10.2 Food Candidates

Retrieve food candidates.

```http
GET /api/v1/food-scanner/candidates
```

This endpoint is currently exposed as a public endpoint in the registered API.

---

## 10.3 Create Scanned Food Item

```http
POST /api/v1/food-scanner/items
```

This endpoint requires authentication.

---

# 11. User Profile

User profile and account management endpoints are available under:

```text
/api/v1/users
```

## Get Profile

```http
GET /api/v1/users/me
```

## Update Profile

```http
PATCH /api/v1/users/me
```

## Change Password

```http
PATCH /api/v1/users/me/password
```

## Delete Account

```http
DELETE /api/v1/users/me
```

All account-management operations require authentication.

---

# 12. Complete Demo Flow

A complete manual demonstration can be performed in this order:

```text
1. GET /health
       │
       ▼
2. POST /api/v1/auth/register
       │
       ▼
3. POST /api/v1/auth/login
       │
       ▼
4. Save access token
       │
       ▼
5. GET /api/v1/auth/me
       │
       ▼
6. POST /api/v1/workouts
       │
       ▼
7. GET /api/v1/workouts
       │
       ▼
8. POST /api/v1/meals
       │
       ▼
9. POST /api/v1/meals/{meal_id}/items
       │
       ▼
10. POST /api/v1/supplements
       │
       ▼
11. POST /api/v1/progress
       │
       ▼
12. GET /api/v1/dashboard/today
       │
       ▼
13. GET /api/v1/dashboard/summary
       │
       ▼
14. GET /api/v1/statistics
       │
       ▼
15. POST /api/v1/food-scanner/scan
       │
       ▼
16. GET /api/v1/users/me
```

This flow demonstrates the main functional areas of the backend without requiring a frontend.

---

# 13. Swagger Demo

The easiest way to demonstrate the API interactively is through Swagger UI.

Open:

```text
http://127.0.0.1:8000/docs
```

The available API groups are organized using the following tags:

```text
Authentication
Workouts
Meals
Supplements
Food Scanner
Progress
Dashboard
Statistics
Users
Health
```

Swagger provides:

* Endpoint discovery
* Request schema inspection
* Response schema inspection
* Authentication testing
* Interactive API execution

For a manual demo, Swagger should be used to inspect the exact request schemas before sending requests.

---

# 14. ReDoc

The alternative API documentation interface is available at:

```text
http://127.0.0.1:8000/redoc
```

The raw OpenAPI specification is available at:

```text
http://127.0.0.1:8000/openapi.json
```

---

# 15. Important Demo Notes

### Authentication

Protected endpoints require a valid JWT access token.

### User Ownership

User-owned resources are scoped to the authenticated user.

### Validation

Invalid request data is rejected through Pydantic/FastAPI validation.

### Rate Limiting

Sensitive endpoints may return:

```http
429 Too Many Requests
```

when their configured rate limit is exceeded.

### File Uploads

Food scanner image uploads are validated before processing.

### Errors

Application errors are handled through the centralized exception-handling system.

---

# 16. API Architecture During the Demo

The demo follows the same layered architecture used by the application:

```text
Client / Swagger
       │
       ▼
FastAPI Router
       │
       ▼
Authentication / Validation
       │
       ▼
Service Layer
       │
       ▼
Repository Layer
       │
       ▼
SQLAlchemy
       │
       ▼
PostgreSQL
```

For integrations such as food recognition and nutrition lookup, additional provider-specific layers are used.

---

# 17. Demo Checklist

Before presenting the project, verify:

```text
[ ] API starts successfully
[ ] GET /health returns OK
[ ] Swagger opens successfully
[ ] User registration works
[ ] Login returns an access token
[ ] Protected endpoints accept the token
[ ] Workout creation works
[ ] Meal creation works
[ ] Meal item creation works
[ ] Supplement creation works
[ ] Progress creation works
[ ] Dashboard endpoints work
[ ] Statistics endpoint works
[ ] Food scanner endpoint is available
[ ] User profile endpoint works
[ ] Error responses are handled correctly
[ ] Rate limiting is active
[ ] Tests pass
```

---

# 18. Current API Scope

The current registered API consists of:

```text
Authentication
Workouts
Meals
Supplements
Food Scanner
Progress
Dashboard
Statistics
Users
Health
```

The reminder implementation exists inside the project, but the reminder router is not currently registered in `app/main.py`; therefore reminder endpoints are not included in this public API demo.

---

# 19. Conclusion

Psych provides a layered fitness and nutrition backend with:

* JWT authentication
* User profiles and account management
* Workout tracking
* Meal and meal-item management
* Nutrition lookup
* Supplement tracking
* Progress tracking and analytics
* Dashboard data
* Fitness/nutrition statistics
* Food image scanning
* Centralized error handling
* Logging
* Rate limiting
* Scheduled application services
* Automated tests
* Interactive OpenAPI documentation

The API can be demonstrated independently through Swagger without requiring a frontend application.
