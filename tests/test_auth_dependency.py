from datetime import timedelta

import pytest
from fastapi import HTTPException

from app.api.v1.deps import get_current_user
from app.core.security import create_access_token
from app.models.user import User


class FakeCredentials:
    def __init__(self, token: str):
        self.credentials = token


def test_get_current_user_with_valid_token():
    user = User(
        id=999999,
        email="security-test@example.com",
        hashed_password="fake-hash",
    )

    class FakeRepository:
        def get_by_id(self, user_id):
            assert user_id == 999999
            return user

    from unittest.mock import patch

    token = create_access_token(str(user.id))

    with patch(
        "app.api.v1.deps.UserRepository",
        return_value=FakeRepository(),
    ):
        result = get_current_user(
            credentials=FakeCredentials(token),
            db=None,
        )

    assert result.id == user.id
    assert result.email == user.email


def test_get_current_user_with_invalid_token():
    credentials = FakeCredentials("invalid-token")

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=credentials,
            db=None,
        )

    assert exc_info.value.status_code == 401


def test_get_current_user_with_expired_token():
    token = create_access_token(
        "999999",
        expires_delta=timedelta(seconds=-1),
    )

    credentials = FakeCredentials(token)

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=credentials,
            db=None,
        )

    assert exc_info.value.status_code == 401


def test_get_current_user_with_nonexistent_user():
    class FakeRepository:
        def get_by_id(self, user_id):
            assert user_id == 999999
            return None

    from unittest.mock import patch

    token = create_access_token("999999")

    with patch(
        "app.api.v1.deps.UserRepository",
        return_value=FakeRepository(),
    ):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(
                credentials=FakeCredentials(token),
                db=None,
            )

    assert exc_info.value.status_code == 401