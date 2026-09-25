import uuid

from sqlalchemy import select

from app.core.database import SessionLocal, get_db
from app.models.user import User


def test_transaction_commit():
    email = f"transaction_commit_{uuid.uuid4().hex}@example.com"

    generator = get_db()
    db = next(generator)

    try:
        user = User(
            email=email,
            hashed_password="transaction-test-password",
        )

        db.add(user)

        try:
            next(generator)
        except StopIteration:
            pass

        check_db = SessionLocal()
        try:
            saved_user = check_db.scalar(
                select(User).where(User.email == email)
            )
            assert saved_user is not None
        finally:
            check_db.close()

    finally:
        generator.close()

        cleanup_db = SessionLocal()
        try:
            user = cleanup_db.scalar(
                select(User).where(User.email == email)
            )

            if user:
                cleanup_db.delete(user)
                cleanup_db.commit()
        finally:
            cleanup_db.close()


def test_transaction_rollback():
    email = f"transaction_rollback_{uuid.uuid4().hex}@example.com"

    generator = get_db()
    db = next(generator)

    try:
        user = User(
            email=email,
            hashed_password="transaction-test-password",
        )

        db.add(user)

        try:
            generator.throw(RuntimeError("forced transaction failure"))
        except RuntimeError:
            pass

        check_db = SessionLocal()
        try:
            saved_user = check_db.scalar(
                select(User).where(User.email == email)
            )
            assert saved_user is None
        finally:
            check_db.close()

    finally:
        generator.close()