from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import TokenResponse, UserResponse, UserCreate


class AuthService:

    def __init__(self, db: Session):
        self.user_repository = UserResponse(db)

    def register(self, user_data: UserCreate) -> UserResponse:
        existing_user = self.user_repository.get_by_email(
            user_data.email
        )

        if existing_user is not None:
            raise ValueError("Email is already registered")

        user = User(
            email=str(user_data.email),
            hashed_password=hash_password(user_data.password),
        )

        created_user = self.user_repository.create(user)

        return UserResponse.model_validate(created_user)

    def login(self, email: str, password: str) -> TokenResponse:
        user = self.user_repository.get_by_email(email)

        if user is None:
            raise ValueError("Invalid email or password")

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise ValueError("Invalid email or password")

        access_token = create_access_token(
            subject=str(user.id)
        )

        return TokenResponse(
            access_token=access_token,
        )