from datetime import date, timedelta
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.main import app
from app.api.v1.deps import get_current_user
from app.api.v1.dashboard import get_dashboard_service
from app.models.user import User
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    DashboardTodayResponse,
)


client = TestClient(app)


def override_current_user(user_id: int):
    def dependency():
        return User(
            id=user_id,
            email=f"user{user_id}@test.com",
            hashed_password="fake-hash",
        )

    return dependency


def setup_user(user_id: int):
    app.dependency_overrides[get_current_user] = (
        override_current_user(user_id)
    )


def teardown_dependencies():
    app.dependency_overrides.clear()


def make_service():
    return Mock()


def test_get_today_dashboard():
    setup_user(1)

    service = make_service()

    service.get_today.return_value = DashboardTodayResponse(
        date=date(2026, 9, 15),
        calories=2200.0,
        protein=150.0,
        workout_duration_minutes=60,
        active_supplements=3,
        total_supplements=5,
        latest_progress_date=date(2026, 9, 14),
    )

    app.dependency_overrides[get_dashboard_service] = (
        lambda: service
    )

    response = client.get("/api/v1/dashboard/today")

    assert response.status_code == 200

    data = response.json()

    assert data["date"] == "2026-09-15"
    assert data["calories"] == 2200.0
    assert data["protein"] == 150.0
    assert data["workout_duration_minutes"] == 60
    assert data["active_supplements"] == 3
    assert data["total_supplements"] == 5
    assert data["latest_progress_date"] == "2026-09-14"

    service.get_today.assert_called_once_with(user_id=1)

    teardown_dependencies()


def test_get_today_dashboard_without_progress():
    setup_user(1)

    service = make_service()

    service.get_today.return_value = DashboardTodayResponse(
        date=date(2026, 9, 15),
        calories=0.0,
        protein=0.0,
        workout_duration_minutes=0,
        active_supplements=0,
        total_supplements=0,
        latest_progress_date=None,
    )

    app.dependency_overrides[get_dashboard_service] = (
        lambda: service
    )

    response = client.get("/api/v1/dashboard/today")

    assert response.status_code == 200

    data = response.json()

    assert data["calories"] == 0.0
    assert data["protein"] == 0.0
    assert data["workout_duration_minutes"] == 0
    assert data["active_supplements"] == 0
    assert data["total_supplements"] == 0
    assert data["latest_progress_date"] is None

    teardown_dependencies()


def test_get_dashboard_summary():
    setup_user(1)

    service = make_service()

    service.get_summary.return_value = DashboardSummaryResponse(
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 7),
        total_calories=14000.0,
        total_protein=900.0,
        total_workout_duration_minutes=300,
        active_supplements=3,
        total_supplements=5,
        latest_progress_date=date(2026, 9, 6),
    )

    app.dependency_overrides[get_dashboard_service] = (
        lambda: service
    )

    response = client.get(
        "/api/v1/dashboard/summary"
        "?start_date=2026-09-01"
        "&end_date=2026-09-07"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["start_date"] == "2026-09-01"
    assert data["end_date"] == "2026-09-07"
    assert data["total_calories"] == 14000.0
    assert data["total_protein"] == 900.0
    assert data["total_workout_duration_minutes"] == 300
    assert data["active_supplements"] == 3
    assert data["total_supplements"] == 5
    assert data["latest_progress_date"] == "2026-09-06"

    service.get_summary.assert_called_once_with(
        user_id=1,
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 7),
    )

    teardown_dependencies()


def test_get_dashboard_summary_with_default_dates():
    setup_user(1)

    service = make_service()

    service.get_summary.return_value = DashboardSummaryResponse(
        start_date=date.today() - timedelta(days=6),
        end_date=date.today(),
        total_calories=0.0,
        total_protein=0.0,
        total_workout_duration_minutes=0,
        active_supplements=0,
        total_supplements=0,
        latest_progress_date=None,
    )

    app.dependency_overrides[get_dashboard_service] = (
        lambda: service
    )

    response = client.get("/api/v1/dashboard/summary")

    assert response.status_code == 200

    service.get_summary.assert_called_once()

    call = service.get_summary.call_args.kwargs

    assert call["user_id"] == 1
    assert call["end_date"] == date.today()
    assert call["start_date"] == date.today() - timedelta(days=6)

    teardown_dependencies()


def test_get_dashboard_summary_with_only_end_date():
    setup_user(1)

    service = make_service()

    service.get_summary.return_value = DashboardSummaryResponse(
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 7),
        total_calories=0.0,
        total_protein=0.0,
        total_workout_duration_minutes=0,
        active_supplements=0,
        total_supplements=0,
        latest_progress_date=None,
    )

    app.dependency_overrides[get_dashboard_service] = (
        lambda: service
    )

    response = client.get(
        "/api/v1/dashboard/summary"
        "?end_date=2026-09-07"
    )

    assert response.status_code == 200

    call = service.get_summary.call_args.kwargs

    assert call["user_id"] == 1
    assert call["end_date"] == date(2026, 9, 7)
    assert call["start_date"] == date(2026, 9, 1)

    teardown_dependencies()


def test_get_dashboard_summary_invalid_date_range():
    setup_user(1)

    service = make_service()

    app.dependency_overrides[get_dashboard_service] = (
        lambda: service
    )

    response = client.get(
        "/api/v1/dashboard/summary"
        "?start_date=2026-09-10"
        "&end_date=2026-09-01"
    )

    assert response.status_code == 400

    assert response.json()["error"]["message"] == (
        "start_date must be before or equal to end_date"
    )

    teardown_dependencies()


def test_dashboard_requires_authentication():
    app.dependency_overrides.clear()

    response = client.get("/api/v1/dashboard/today")

    assert response.status_code in (401, 403)

    app.dependency_overrides.clear()