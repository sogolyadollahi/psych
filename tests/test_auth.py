from datetime import datetime, timedelta, timezone
import jwt
import pytest

from app.core.config import settings
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_and_verify():
    password = "MySecretPassword123"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword123", hashed) is False


def test_create_and_decode_access_token():
    user_id = "123"

    token = create_access_token(user_id)
    payload = decode_access_token(token)

    assert payload["sub"] == user_id
    assert "exp" in payload


def test_expired_access_token():
    token = create_access_token(
        "123",
        expires_delta=timedelta(seconds=-1),
    )

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(token)


def test_invalid_access_token():
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token("this-is-not-a-valid-jwt")


def test_token_without_subject():
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    decoded = decode_access_token(token)

    assert decoded.get("sub") is None