from datetime import date, datetime
from unittest.mock import Mock

import pytest

from app.services.dashboard_service import DashboardService


def make_meal(
    meal_date,
    calories,
    protein,
):
    item = Mock()
    item.calories = calories
    item.protein = protein

    meal = Mock()
    meal.meal_date = meal_date
    meal.items = [item]

    return meal


def make_workout(
    workout_date,
    duration_minutes,
):
    workout = Mock()
    workout.workout_date = workout_date
    workout.duration_minutes = duration_minutes
    return workout


def make_supplement(is_active):
    supplement = Mock()
    supplement.is_active = is_active
    return supplement


def make_progress(progress_date):
    progress = Mock()
    progress.progress_date = progress_date
    return progress


@pytest.fixture
def repositories():
    return {
        "meal": Mock(),
        "workout": Mock(),
        "supplement": Mock(),
        "progress": Mock(),
    }


@pytest.fixture
def service(repositories):
    return DashboardService(
        meal_repository=repositories["meal"],
        workout_repository=repositories["workout"],
        supplement_repository=repositories["supplement"],
        progress_repository=repositories["progress"],
    )


def test_get_today_returns_today_summary(service, repositories, monkeypatch):
    today = date(2026, 9, 15)

    monkeypatch.setattr(
        "app.services.dashboard_service.date",
        type(
            "MockDate",
            (),
            {
                "today": staticmethod(lambda: today),
            },
        ),
    )

    repositories["meal"].get_by_user_id.return_value = [
        make_meal(today, 500, 30),
        make_meal(today, 700, 50),
        make_meal(date(2026, 9, 14), 999, 99),
    ]

    repositories["workout"].get_by_user_id.return_value = [
        make_workout(datetime(2026, 9, 15, 10, 0), 45),
        make_workout(datetime(2026, 9, 14, 10, 0), 90),
    ]

    repositories["supplement"].get_by_user_id.return_value = [
        make_supplement(True),
        make_supplement(True),
        make_supplement(False),
    ]

    repositories["progress"].get_by_user_id.return_value = [
        make_progress(today),
        make_progress(date(2026, 9, 10)),
    ]

    result = service.get_today(user_id=1)

    assert result.date == today
    assert result.calories == 1200.0
    assert result.protein == 80.0
    assert result.workout_duration_minutes == 45
    assert result.active_supplements == 2
    assert result.total_supplements == 3
    assert result.latest_progress_date == today


def test_get_today_without_progress(service, repositories, monkeypatch):
    today = date(2026, 9, 15)

    monkeypatch.setattr(
        "app.services.dashboard_service.date",
        type(
            "MockDate",
            (),
            {
                "today": staticmethod(lambda: today),
            },
        ),
    )

    repositories["meal"].get_by_user_id.return_value = []
    repositories["workout"].get_by_user_id.return_value = []
    repositories["supplement"].get_by_user_id.return_value = []
    repositories["progress"].get_by_user_id.return_value = []

    result = service.get_today(user_id=1)

    assert result.calories == 0.0
    assert result.protein == 0.0
    assert result.workout_duration_minutes == 0
    assert result.active_supplements == 0
    assert result.total_supplements == 0
    assert result.latest_progress_date is None


def test_get_summary_returns_aggregated_data(service, repositories):
    start_date = date(2026, 9, 1)
    end_date = date(2026, 9, 7)

    repositories["meal"].get_by_user_id.return_value = [
        make_meal(date(2026, 9, 1), 500, 30),
        make_meal(date(2026, 9, 5), 700, 40),
        make_meal(date(2026, 9, 10), 999, 99),
    ]

    repositories["workout"].get_by_user_id.return_value = [
        make_workout(datetime(2026, 9, 2, 10, 0), 45),
        make_workout(datetime(2026, 9, 6, 10, 0), 30),
        make_workout(datetime(2026, 9, 10, 10, 0), 90),
    ]

    repositories["supplement"].get_by_user_id.return_value = [
        make_supplement(True),
        make_supplement(False),
        make_supplement(True),
    ]

    repositories["progress"].get_by_user_id_and_date_range.return_value = [
        make_progress(date(2026, 9, 2)),
        make_progress(date(2026, 9, 6)),
    ]

    result = service.get_summary(
        user_id=1,
        start_date=start_date,
        end_date=end_date,
    )

    assert result.start_date == start_date
    assert result.end_date == end_date
    assert result.total_calories == 1200.0
    assert result.total_protein == 70.0
    assert result.total_workout_duration_minutes == 75
    assert result.active_supplements == 2
    assert result.total_supplements == 3
    assert result.latest_progress_date == date(2026, 9, 6)


def test_get_summary_filters_date_range(service, repositories):
    start_date = date(2026, 9, 1)
    end_date = date(2026, 9, 7)

    repositories["meal"].get_by_user_id.return_value = [
        make_meal(date(2026, 8, 31), 1000, 100),
        make_meal(date(2026, 9, 3), 500, 30),
        make_meal(date(2026, 9, 8), 1000, 100),
    ]

    repositories["workout"].get_by_user_id.return_value = [
        make_workout(datetime(2026, 8, 31, 10, 0), 100),
        make_workout(datetime(2026, 9, 3, 10, 0), 40),
        make_workout(datetime(2026, 9, 8, 10, 0), 100),
    ]

    repositories["supplement"].get_by_user_id.return_value = []
    repositories["progress"].get_by_user_id_and_date_range.return_value = []

    result = service.get_summary(
        user_id=1,
        start_date=start_date,
        end_date=end_date,
    )

    assert result.total_calories == 500.0
    assert result.total_protein == 30.0
    assert result.total_workout_duration_minutes == 40


def test_get_summary_invalid_date_range(service, repositories):
    with pytest.raises(
        ValueError,
        match="start_date must be before or equal to end_date",
    ):
        service.get_summary(
            user_id=1,
            start_date=date(2026, 9, 10),
            end_date=date(2026, 9, 1),
        )
