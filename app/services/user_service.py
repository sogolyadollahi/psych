from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.user import (
    ChangePasswordRequest,
    UserProfileUpdate,
)


class UserService:
    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # User Profile
    # =====================================================

    def get_profile(
        self,
        current_user: User,
    ) -> User:
        return current_user

    def update_profile(
        self,
        current_user: User,
        profile_data: UserProfileUpdate,
    ) -> User:
        update_data = profile_data.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(current_user, field, value)

        self.db.flush()
        self.db.refresh(current_user)

        return current_user

    # =====================================================
    # Account Management - Change Password
    # =====================================================

    def change_password(
        self,
        current_user: User,
        password_data: ChangePasswordRequest,
    ) -> None:
        # 1. Verify current password
        is_current_password_valid = verify_password(
            password_data.current_password,
            current_user.hashed_password,
        )

        if not is_current_password_valid:
            raise ValueError(
                "Current password is incorrect"
            )

        # 2. Prevent reusing the current password
        is_same_password = verify_password(
            password_data.new_password,
            current_user.hashed_password,
        )

        if is_same_password:
            raise ValueError(
                "New password must be different from "
                "current password"
            )

        # 3. Hash the new password
        new_hashed_password = hash_password(
            password_data.new_password,
        )

        # 4. Update the password hash
        current_user.hashed_password = (
            new_hashed_password
        )

        # Make the change visible inside the current transaction.
        # Final commit is handled by get_db().
        self.db.flush()

    # =====================================================
    # Account Management - Delete Account
    # =====================================================

    def delete_account(
        self,
        current_user: User,
    ) -> None:
        self.db.delete(current_user)

        # Final commit is handled by get_db().
        self.db.flush()