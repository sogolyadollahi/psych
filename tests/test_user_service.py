from datetime import datetime
from unittest.mock import Mock

from app.models.user import User
from app.schemas.user import UserProfileUpdate
from app.services.user_service import UserService


def make_user():
    return User(
        id=1,
        email="test@example.com",
        hashed_password="fake-hash",
        first_name="Ali",
        last_name="Ahmadi",
        age=25,
        gender="male",
        height_cm=180,
        activity_level="moderate",
        goal="muscle_gain",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def test_get_profile():
    db = Mock()
    service = UserService(db)

    user = make_user()

    result = service.get_profile(user)

    assert result is user


def test_update_profile():
    db = Mock()
    service = UserService(db)

    user = make_user()

    update_data = UserProfileUpdate(
        first_name="Reza",
        height_cm=185,
        goal="fat_loss",
    )

    result = service.update_profile(
        current_user=user,
        profile_data=update_data,
    )

    assert result.first_name == "Reza"
    assert result.height_cm == 185
    assert result.goal == "fat_loss"

    # فیلدهای دیگر نباید تغییر کنند
    assert result.last_name == "Ahmadi"
    assert result.age == 25
    assert result.gender == "male"

    db.flush.assert_called_once()
    db.refresh.assert_called_once_with(user)


def test_update_profile_only_changes_provided_fields():
    db = Mock()
    service = UserService(db)

    user = make_user()

    update_data = UserProfileUpdate(
        height_cm=190,
    )

    service.update_profile(
        current_user=user,
        profile_data=update_data,
    )

    assert user.height_cm == 190
    assert user.first_name == "Ali"
    assert user.last_name == "Ahmadi"
    assert user.age == 25
    assert user.goal == "muscle_gain"