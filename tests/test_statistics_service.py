from datetime import date, datetime
from unittest.mock import Mock

import pytest

from app.services.statistics_service import StatisticsService


def make_meal(meal_date, items):
    meal = Mock()
    meal.meal_date = meal_date
    meal.items = items
    return meal


def make_item(calories, protein):
    item = Mock()
    item.calories = calories
    item.protein = protein
    return item


def make_workout(workout_date, duration_minutes, calories_burned):
    workout = Mock()
    workout.workout_date = workout_date
    workout.duration_minutes = duration_minutes
    workout.calories_burned = calories_burned
    return workout


def make_progress(
    progress_date,
    weight=None,
    body_fat=None,
    chest=None,
    waist=None,
    arm=None,
    thigh=None,
):
    progress = Mock()
    progress.progress_date = progress_date
    progress.weight = weight
    progress.body_fat = body_fat
    progress.chest = chest
    progress.waist = waist
    progress.arm = arm
    progress.thigh = thigh
    return progress


@pytest.fixture
def repositories():
    return {
        "meal": Mock(),
        "workout": Mock(),
        "progress": Mock(),
    }


@pytest.fixture
def service(repositories):
    return StatisticsService(
        meal_repository=repositories["meal"],
        workout_repository=repositories["workout"],
        progress_repository=repositories["progress"],
    )


def test_get_statistics_returns_nutrition_by_date(service, repositories):
    repositories["meal"].get_by_user_id.return_value = [
        make_meal(
            date(2026, 9, 1),
            [
                make_item(500, 30),
                make_item(300, 20),
            ],
        ),
        make_meal(
            date(2026, 9, 1),
            [
                make_item(200, 10),
            ],
        ),
        make_meal(
            date(2026, 9, 2),
            [
                make_item(700, 40),
            ],
        ),
    ]

    repositories["workout"].get_by_user_id.return_value = []
    repositories["progress"].get_by_user_id_and_date_range.return_value = []

    result = service.get_statistics(
        user_id=1,
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 2),
    )

    assert len(result.nutrition) == 2

    assert result.nutrition[0].date == date(2026, 9, 1)
    assert result.nutrition[0].calories == 1000.0
    assert result.nutrition[0].protein == 60.0

    assert result.nutrition[1].date == date(2026, 9, 2)
    assert result.nutrition[1].calories == 700.0
    assert result.nutrition[1].protein == 40.0


def test_get_statistics_filters_nutrition_by_date_range(
    service,
    repositories,
):
    repositories["meal"].get_by_user_id.return_value = [
        make_meal(
            date(2026, 8, 31),
            [make_item(1000, 100)],
        ),
        make_meal(
            date(2026, 9, 2),
            [make_item(500, 30)],
        ),
        make_meal(
            date(2026, 9, 8),
            [make_item(1000, 100)],
        ),
    ]

    repositories["workout"].get_by_user_id.return_value = []
    repositories["progress"].get_by_user_id_and_date_range.return_value = []

    result = service.get_statistics(
        user_id=1,
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 7),
    )

    assert len(result.nutrition) == 1
    assert result.nutrition[0].date == date(2026, 9, 2)
    assert result.nutrition[0].calories == 500.0
    assert result.nutrition[0].protein == 30.0


def test_get_statistics_returns_workout_by_date(service, repositories):
    repositories["meal"].get_by_user_id.return_value = []

    repositories["workout"].get_by_user_id.return_value = [
        make_workout(
            datetime(2026, 9, 1, 10, 0),
            45,
            300,
        ),
        make_workout(
            datetime(2026, 9, 1, 18, 0),
            30,
            200,
        ),
        make_workout(
            datetime(2026, 9, 2, 12, 0),
            60,
            400,
        ),
    ]

    repositories["progress"].get_by_user_id_and_date_range.return_value = []

    result = service.get_statistics(
        user_id=1,
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 2),
    )

    assert len(result.workouts) == 2

    assert result.workouts[0].date == date(2026, 9, 1)
    assert result.workouts[0].duration_minutes == 75
    assert result.workouts[0].calories_burned == 500

    assert result.workouts[1].date == date(2026, 9, 2)
    assert result.workouts[1].duration_minutes == 60
    assert result.workouts[1].calories_burned == 400


def test_get_statistics_returns_progress(service, repositories):
    repositories["meal"].get_by_user_id.return_value = []
    repositories["workout"].get_by_user_id.return_value = []

    repositories["progress"].get_by_user_id_and_date_range.return_value = [
        make_progress(
            date(2026, 9, 1),
            weight=80,
            body_fat=20,
            chest=100,
            waist=85,
            arm=35,
            thigh=55,
        ),
        make_progress(
            date(2026, 9, 5),
            weight=79,
            body_fat=19,
            chest=101,
            waist=83,
            arm=35.5,
            thigh=54,
        ),
    ]

    result = service.get_statistics(
        user_id=1,
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 7),
    )

    assert len(result.progress) == 2

    assert result.progress[0].date == date(2026, 9, 1)
    assert result.progress[0].weight == 80.0
    assert result.progress[0].body_fat == 20.0
    assert result.progress[0].chest == 100.0
    assert result.progress[0].waist == 85.0
    assert result.progress[0].arm == 35.0
    assert result.progress[0].thigh == 55.0

    assert result.progress[1].weight == 79.0
    assert result.progress[1].body_fat == 19.0


def test_get_statistics_handles_none_progress_values(
    service,
    repositories,
):
    repositories["meal"].get_by_user_id.return_value = []
    repositories["workout"].get_by_user_id.return_value = []

    repositories["progress"].get_by_user_id_and_date_range.return_value = [
        make_progress(
            date(2026, 9, 1),
            weight=80,
            body_fat=None,
            chest=None,
            waist=85,
            arm=None,
            thigh=55,
        )
    ]

    result = service.get_statistics(
        user_id=1,
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 1),
    )

    record = result.progress[0]

    assert record.weight == 80.0
    assert record.body_fat is None
    assert record.chest is None
    assert record.waist == 85.0
    assert record.arm is None
    assert record.thigh == 55.0


def test_get_statistics_returns_empty_lists_when_no_data(
    service,
    repositories,
):
    repositories["meal"].get_by_user_id.return_value = []
    repositories["workout"].get_by_user_id.return_value = []
    repositories["progress"].get_by_user_id_and_date_range.return_value = []

    result = service.get_statistics(
        user_id=1,
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 7),
    )

    assert result.nutrition == []
    assert result.workouts == []
    assert result.progress == []


def test_get_statistics_invalid_date_range(service, repositories):
    with pytest.raises(
        ValueError,
        match="start_date must be before or equal to end_date",
    ):
        service.get_statistics(
            user_id=1,
            start_date=date(2026, 9, 10),
            end_date=date(2026, 9, 1),
        )
