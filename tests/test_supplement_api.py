from datetime import datetime, time

from fastapi.testclient import TestClient

from app.main import app
from app.api.v1.deps import get_current_user
from app.api.v1.supplement_deps import get_supplement_service
from app.models.user import User
from app.models.supplement import Supplement


client = TestClient(app)


# =========================================================
# Helpers
# =========================================================

def override_current_user(user_id: int):
    def dependency():
        user = User(
            id=user_id,
            email=f"user{user_id}@test.com",
            hashed_password="fake-hash",
        )

        return user

    return dependency


def create_supplement(
    supplement_id=1,
    user_id=1,
):
    return Supplement(
        id=supplement_id,
        user_id=user_id,
        name="Creatine",
        dosage="5g",
        reminder_time=time(14, 0),
        notes="After workout",
        is_active=True,
        created_at=datetime(2026, 8, 22, 12, 0, 0),
    )


# =========================================================
# Mock Service
# =========================================================

class MockSupplementService:

    def __init__(self):
        self.supplements = {}

    def create_supplement(
        self,
        user_id: int,
        name: str,
        dosage: str,
        reminder_time: time,
        notes: str | None = None,
    ):
        supplement = Supplement(
            id=1,
            user_id=user_id,
            name=name,
            dosage=dosage,
            reminder_time=reminder_time,
            notes=notes,
            is_active=True,
            created_at=datetime.now(),
        )

        self.supplements[1] = supplement

        return supplement

    def get_user_supplements(
        self,
        user_id: int,
    ):
        return [
            supplement
            for supplement in self.supplements.values()
            if supplement.user_id == user_id
        ]

    def get_supplement(
        self,
        supplement_id: int,
        user_id: int,
    ):
        supplement = self.supplements.get(supplement_id)

        if supplement is None:
            return None

        if supplement.user_id != user_id:
            return None

        return supplement

    def update_supplement(
        self,
        supplement: Supplement,
        name: str | None = None,
        dosage: str | None = None,
        reminder_time: time | None = None,
        notes: str | None = None,
        is_active: bool | None = None,
    ):
        if name is not None:
            supplement.name = name

        if dosage is not None:
            supplement.dosage = dosage

        if reminder_time is not None:
            supplement.reminder_time = reminder_time

        if notes is not None:
            supplement.notes = notes

        if is_active is not None:
            supplement.is_active = is_active

        return supplement

    def delete_supplement(
        self,
        supplement: Supplement,
    ):
        self.supplements.pop(
            supplement.id,
            None,
        )


# =========================================================
# Fixtures / Setup
# =========================================================

def setup_service(
    supplements: list[Supplement] | None = None,
):
    service = MockSupplementService()

    if supplements:
        for supplement in supplements:
            service.supplements[supplement.id] = supplement

    app.dependency_overrides[
        get_supplement_service
    ] = lambda: service

    return service


def teardown_dependencies():
    app.dependency_overrides.clear()


# =========================================================
# CREATE
# =========================================================

def test_create_supplement():
    service = setup_service()

    app.dependency_overrides[
        get_current_user
    ] = override_current_user(1)

    response = client.post(
        "/api/v1/supplements",
        json={
            "name": "Creatine",
            "dosage": "5g",
            "reminder_time": "14:00:00",
            "notes": "After workout",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Creatine"
    assert data["dosage"] == "5g"
    assert data["reminder_time"] == "14:00:00"
    assert data["notes"] == "After workout"
    assert data["is_active"] is True
    assert data["created_at"] is not None

    teardown_dependencies()


# =========================================================
# GET LIST
# =========================================================

def test_get_supplements():
    supplements = [
        create_supplement(
            supplement_id=1,
            user_id=1,
        ),
        Supplement(
            id=2,
            user_id=1,
            name="Vitamin D",
            dosage="1000 IU",
            reminder_time=time(9, 0),
            notes=None,
            is_active=True,
            created_at=datetime(2026, 8, 22, 12, 0, 0),
        ),
        Supplement(
            id=3,
            user_id=2,
            name="Omega 3",
            dosage="1g",
            reminder_time=time(12, 0),
            notes=None,
            is_active=True,
            created_at=datetime(2026, 8, 22, 12, 0, 0),
        ),
    ]

    setup_service(supplements)

    app.dependency_overrides[
        get_current_user
    ] = override_current_user(1)

    response = client.get(
        "/api/v1/supplements",
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert all(
        supplement["id"] in [1, 2]
        for supplement in data
    )

    teardown_dependencies()


# =========================================================
# GET SINGLE - OWNER
# =========================================================

def test_get_supplement_owner():
    supplement = create_supplement(
        supplement_id=1,
        user_id=1,
    )

    setup_service([supplement])

    app.dependency_overrides[
        get_current_user
    ] = override_current_user(1)

    response = client.get(
        "/api/v1/supplements/1",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Creatine"

    teardown_dependencies()


# =========================================================
# GET SINGLE - OTHER USER
# =========================================================

def test_get_supplement_other_user_cannot_access():
    supplement = create_supplement(
        supplement_id=1,
        user_id=1,
    )

    setup_service([supplement])

    app.dependency_overrides[
        get_current_user
    ] = override_current_user(2)

    response = client.get(
        "/api/v1/supplements/1",
    )

    assert response.status_code == 404

    assert response.json()["error"]["message"] == (
        "Supplement not found"
    )

    teardown_dependencies()


# =========================================================
# UPDATE - OWNER
# =========================================================

def test_update_supplement():
    supplement = create_supplement(
        supplement_id=1,
        user_id=1,
    )

    setup_service([supplement])

    app.dependency_overrides[
        get_current_user
    ] = override_current_user(1)

    response = client.patch(
        "/api/v1/supplements/1",
        json={
            "name": "Creatine Monohydrate",
            "dosage": "10g",
            "reminder_time": "15:00:00",
            "notes": "Updated note",
            "is_active": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Creatine Monohydrate"
    assert data["dosage"] == "10g"
    assert data["reminder_time"] == "15:00:00"
    assert data["notes"] == "Updated note"
    assert data["is_active"] is False

    teardown_dependencies()


# =========================================================
# UPDATE - OTHER USER
# =========================================================

def test_update_supplement_other_user_cannot_access():
    supplement = create_supplement(
        supplement_id=1,
        user_id=1,
    )

    setup_service([supplement])

    app.dependency_overrides[
        get_current_user
    ] = override_current_user(2)

    response = client.patch(
        "/api/v1/supplements/1",
        json={
            "name": "Hacked Supplement",
        },
    )

    assert response.status_code == 404

    assert response.json()["error"]["message"] == (
        "Supplement not found"
    )

    teardown_dependencies()


# =========================================================
# DELETE - OWNER
# =========================================================

def test_delete_supplement():
    supplement = create_supplement(
        supplement_id=1,
        user_id=1,
    )

    service = setup_service([supplement])

    app.dependency_overrides[
        get_current_user
    ] = override_current_user(1)

    response = client.delete(
        "/api/v1/supplements/1",
    )

    assert response.status_code == 204

    assert 1 not in service.supplements

    teardown_dependencies()


# =========================================================
# DELETE - OTHER USER
# =========================================================

def test_delete_supplement_other_user_cannot_access():
    supplement = create_supplement(
        supplement_id=1,
        user_id=1,
    )

    service = setup_service([supplement])

    app.dependency_overrides[
        get_current_user
    ] = override_current_user(2)

    response = client.delete(
        "/api/v1/supplements/1",
    )

    assert response.status_code == 404

    assert 1 in service.supplements

    teardown_dependencies()


# =========================================================
# UNAUTHORIZED
# =========================================================

def test_create_supplement_requires_authentication():
    setup_service()

    response = client.post(
        "/api/v1/supplements",
        json={
            "name": "Creatine",
            "dosage": "5g",
            "reminder_time": "14:00:00",
            "notes": None,
        },
    )

    assert response.status_code == 403

    teardown_dependencies()