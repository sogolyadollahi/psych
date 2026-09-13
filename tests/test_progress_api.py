from datetime import date, datetime
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.api.v1.deps import get_current_user
from app.models.progress import Progress
from app.models.user import User


client = TestClient(app)


# =========================================================
# Helpers
# =========================================================

def override_current_user(user_id: int):
    def dependency():
        return User(
            id=user_id,
            email=f"user{user_id}@test.com",
            hashed_password="fake-hash",
        )

    return dependency


def create_progress(
    progress_id=1,
    user_id=1,
    weight=80.0,
    body_fat=20.0,
    chest=100.0,
    waist=85.0,
    arm=35.0,
    thigh=55.0,
    progress_date=date(2026, 8, 22),
):
    return Progress(
        id=progress_id,
        user_id=user_id,
        weight=weight,
        body_fat=body_fat,
        chest=chest,
        waist=waist,
        arm=arm,
        thigh=thigh,
        progress_date=progress_date,
        created_at=datetime(2026, 8, 22, 12, 0, 0),
        updated_at=datetime(2026, 8, 22, 12, 0, 0),
    )


def setup_user(user_id: int):
    app.dependency_overrides[
        get_current_user
    ] = override_current_user(user_id)


def teardown_dependencies():
    app.dependency_overrides.clear()


# =========================================================
# CREATE
# =========================================================

def test_create_progress():
    progress = create_progress()

    mock_service = patch(
        "app.api.v1.progress.ProgressService"
    )

    with mock_service as service_class:
        service = service_class.return_value
        service.create.return_value = progress

        setup_user(1)

        response = client.post(
            "/api/v1/progress",
            json={
                "weight_kg": 80,
                "body_fat_percentage": 20,
                "chest_cm": 100,
                "waist_cm": 85,
                "arm_cm": 35,
                "thigh_cm": 55,
                "progress_date": "2026-08-22",
            },
        )

        assert response.status_code == 201

        data = response.json()

        assert data["id"] == 1
        assert data["weight_kg"] == 80
        assert data["body_fat_percentage"] == 20
        assert data["chest_cm"] == 100
        assert data["waist_cm"] == 85
        assert data["arm_cm"] == 35
        assert data["thigh_cm"] == 55
        assert data["progress_date"] == "2026-08-22"

        service.create.assert_called_once()

    teardown_dependencies()


# =========================================================
# GET LIST
# =========================================================

def test_get_progress_records():
    records = [
        create_progress(
            progress_id=1,
            user_id=1,
        ),
        create_progress(
            progress_id=2,
            user_id=1,
            weight=78,
            progress_date=date(2026, 8, 25),
        ),
        create_progress(
            progress_id=3,
            user_id=2,
        ),
    ]

    mock_service = patch(
        "app.api.v1.progress.ProgressService"
    )

    with mock_service as service_class:
        service = service_class.return_value
        service.get_all.return_value = records[:2]

        setup_user(1)

        response = client.get(
            "/api/v1/progress",
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[1]["id"] == 2

        service.get_all.assert_called_once()

    teardown_dependencies()


# =========================================================
# GET SINGLE - OWNER
# =========================================================

def test_get_progress_owner():
    progress = create_progress(
        progress_id=1,
        user_id=1,
    )

    with patch(
        "app.api.v1.progress.ProgressService"
    ) as service_class:
        service = service_class.return_value
        service.get_by_id.return_value = progress

        setup_user(1)

        response = client.get(
            "/api/v1/progress/1",
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == 1
        assert data["weight_kg"] == 80

        service.get_by_id.assert_called_once()

    teardown_dependencies()


# =========================================================
# GET SINGLE - OTHER USER
# =========================================================

def test_get_progress_other_user_cannot_access():
    with patch(
        "app.api.v1.progress.ProgressService"
    ) as service_class:
        service = service_class.return_value

        service.get_by_id.side_effect = ValueError(
            "Progress record not found"
        )

        setup_user(2)

        response = client.get(
            "/api/v1/progress/1",
        )

        assert response.status_code == 404

        assert response.json()["detail"] == (
            "Progress record not found"
        )

    teardown_dependencies()


# =========================================================
# GET SINGLE - NOT FOUND
# =========================================================

def test_get_progress_not_found():
    with patch(
        "app.api.v1.progress.ProgressService"
    ) as service_class:
        service = service_class.return_value

        service.get_by_id.side_effect = ValueError(
            "Progress record not found"
        )

        setup_user(1)

        response = client.get(
            "/api/v1/progress/999",
        )

        assert response.status_code == 404

        assert response.json()["detail"] == (
            "Progress record not found"
        )

    teardown_dependencies()


# =========================================================
# ANALYTICS
# =========================================================

def test_get_progress_analytics():
    from app.schemas.progress import ProgressAnalyticsResponse

    analytics = ProgressAnalyticsResponse(
        start_date=date(2026, 8, 1),
        end_date=date(2026, 8, 22),
        weight_change_kg=-2.5,
        body_fat_change_percentage=-1.5,
        chest_change_cm=1.0,
        waist_change_cm=-3.0,
        arm_change_cm=1.0,
        thigh_change_cm=1.0,
    )

    with patch(
        "app.api.v1.progress.ProgressService"
    ) as service_class:
        service = service_class.return_value
        service.get_analytics.return_value = analytics

        setup_user(1)

        response = client.get(
            "/api/v1/progress/analytics",
        )

        assert response.status_code == 200

        data = response.json()

        assert data["start_date"] == "2026-08-01"
        assert data["end_date"] == "2026-08-22"
        assert data["weight_change_kg"] == -2.5
        assert data["body_fat_change_percentage"] == -1.5
        assert data["chest_change_cm"] == 1
        assert data["waist_change_cm"] == -3
        assert data["arm_change_cm"] == 1
        assert data["thigh_change_cm"] == 1

        service.get_analytics.assert_called_once()

    teardown_dependencies()


# =========================================================
# ANALYTICS - DATE RANGE
# =========================================================

def test_get_progress_analytics_with_date_range():
    from app.schemas.progress import ProgressAnalyticsResponse

    analytics = ProgressAnalyticsResponse(
        start_date=date(2026, 8, 10),
        end_date=date(2026, 8, 20),
        weight_change_kg=-2.0,
        body_fat_change_percentage=-1.0,
        chest_change_cm=1.0,
        waist_change_cm=-2.0,
        arm_change_cm=1.0,
        thigh_change_cm=1.0,
    )

    with patch(
        "app.api.v1.progress.ProgressService"
    ) as service_class:
        service = service_class.return_value
        service.get_analytics.return_value = analytics

        setup_user(1)

        response = client.get(
            "/api/v1/progress/analytics",
            params={
                "start_date": "2026-08-10",
                "end_date": "2026-08-20",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["start_date"] == "2026-08-10"
        assert data["end_date"] == "2026-08-20"

        service.get_analytics.assert_called_once()

        call_kwargs = (
            service.get_analytics.call_args.kwargs
        )

        assert call_kwargs["start_date"] == date(
            2026, 8, 10
        )
        assert call_kwargs["end_date"] == date(
            2026, 8, 20
        )

    teardown_dependencies()


# =========================================================
# ANALYTICS - NO RECORDS
# =========================================================

def test_get_progress_analytics_no_records():
    with patch(
        "app.api.v1.progress.ProgressService"
    ) as service_class:
        service = service_class.return_value

        service.get_analytics.side_effect = ValueError(
            "No progress records found for the selected date range"
        )

        setup_user(1)

        response = client.get(
            "/api/v1/progress/analytics",
        )

        assert response.status_code == 404

        assert response.json()["detail"] == (
            "No progress records found for the selected date range"
        )

    teardown_dependencies()


# =========================================================
# UPDATE - OWNER
# =========================================================

def test_update_progress():
    progress = create_progress(
        progress_id=1,
        user_id=1,
        weight=77,
        body_fat=18,
        waist=82,
        progress_date=date(2026, 8, 25),
    )

    with patch(
        "app.api.v1.progress.ProgressService"
    ) as service_class:
        service = service_class.return_value
        service.update.return_value = progress

        setup_user(1)

        response = client.patch(
            "/api/v1/progress/1",
            json={
                "weight_kg": 77,
                "body_fat_percentage": 18,
                "waist_cm": 82,
                "progress_date": "2026-08-25",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["weight_kg"] == 77
        assert data["body_fat_percentage"] == 18
        assert data["waist_cm"] == 82
        assert data["progress_date"] == "2026-08-25"

        service.update.assert_called_once()

    teardown_dependencies()


# =========================================================
# UPDATE - OTHER USER
# =========================================================

def test_update_progress_other_user_cannot_access():
    with patch(
        "app.api.v1.progress.ProgressService"
    ) as service_class:
        service = service_class.return_value

        service.update.side_effect = ValueError(
            "Progress record not found"
        )

        setup_user(2)

        response = client.patch(
            "/api/v1/progress/1",
            json={
                "weight_kg": 50,
            },
        )

        assert response.status_code == 404

        assert response.json()["detail"] == (
            "Progress record not found"
        )

    teardown_dependencies()


# =========================================================
# DELETE - OWNER
# =========================================================

def test_delete_progress():
    with patch(
        "app.api.v1.progress.ProgressService"
    ) as service_class:
        service = service_class.return_value
        service.delete.return_value = None

        setup_user(1)

        response = client.delete(
            "/api/v1/progress/1",
        )

        assert response.status_code == 204

        service.delete.assert_called_once()

    teardown_dependencies()


# =========================================================
# DELETE - OTHER USER
# =========================================================

def test_delete_progress_other_user_cannot_access():
    with patch(
        "app.api.v1.progress.ProgressService"
    ) as service_class:
        service = service_class.return_value

        service.delete.side_effect = ValueError(
            "Progress record not found"
        )

        setup_user(2)

        response = client.delete(
            "/api/v1/progress/1",
        )

        assert response.status_code == 404

        assert response.json()["detail"] == (
            "Progress record not found"
        )

    teardown_dependencies()


# =========================================================
# UNAUTHORIZED
# =========================================================

def test_get_progress_requires_authentication():
    response = client.get(
        "/api/v1/progress",
    )

    assert response.status_code == 403