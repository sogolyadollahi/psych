from datetime import time
from unittest.mock import Mock

from app.models.supplement import Supplement
from app.services.supplement_service import SupplementService


def test_create_supplement():
    repository = Mock()
    service = SupplementService(repository)

    repository.create.side_effect = lambda supplement: supplement

    supplement = service.create_supplement(
        user_id=1,
        name="Creatine",
        dosage="5g",
        reminder_time=time(14, 0),
        notes="After workout",
    )

    assert supplement.user_id == 1
    assert supplement.name == "Creatine"
    assert supplement.dosage == "5g"
    assert supplement.reminder_time == time(14, 0)
    assert supplement.notes == "After workout"
    assert supplement.is_active is True

    repository.create.assert_called_once()


def test_get_supplement_owner_can_access():
    repository = Mock()
    service = SupplementService(repository)

    supplement = Supplement(
        id=1,
        user_id=10,
        name="Creatine",
        dosage="5g",
        reminder_time=time(14, 0),
        notes=None,
        is_active=True,
    )

    repository.get_by_id.return_value = supplement

    result = service.get_supplement(
        supplement_id=1,
        user_id=10,
    )

    assert result == supplement


def test_get_supplement_other_user_cannot_access():
    repository = Mock()
    service = SupplementService(repository)

    supplement = Supplement(
        id=1,
        user_id=10,
        name="Creatine",
        dosage="5g",
        reminder_time=time(14, 0),
        notes=None,
        is_active=True,
    )

    repository.get_by_id.return_value = supplement

    result = service.get_supplement(
        supplement_id=1,
        user_id=99,
    )

    assert result is None


def test_get_user_supplements():
    repository = Mock()
    service = SupplementService(repository)

    supplements = [
        Supplement(
            id=1,
            user_id=10,
            name="Creatine",
            dosage="5g",
            reminder_time=time(14, 0),
            is_active=True,
        ),
        Supplement(
            id=2,
            user_id=10,
            name="Vitamin D",
            dosage="1000 IU",
            reminder_time=time(9, 0),
            is_active=True,
        ),
    ]

    repository.get_by_user_id.return_value = supplements

    result = service.get_user_supplements(
        user_id=10,
    )

    assert result == supplements
    assert len(result) == 2

    repository.get_by_user_id.assert_called_once_with(10)


def test_update_supplement():
    repository = Mock()
    service = SupplementService(repository)

    supplement = Supplement(
        id=1,
        user_id=10,
        name="Creatine",
        dosage="5g",
        reminder_time=time(14, 0),
        notes="Before workout",
        is_active=True,
    )

    repository.update.side_effect = lambda supplement: supplement

    result = service.update_supplement(
        supplement=supplement,
        name="Creatine Monohydrate",
        dosage="10g",
        reminder_time=time(15, 0),
        notes="After workout",
        is_active=False,
    )

    assert result.name == "Creatine Monohydrate"
    assert result.dosage == "10g"
    assert result.reminder_time == time(15, 0)
    assert result.notes == "After workout"
    assert result.is_active is False

    repository.update.assert_called_once_with(supplement)


def test_delete_supplement():
    repository = Mock()
    service = SupplementService(repository)

    supplement = Supplement(
        id=1,
        user_id=10,
        name="Creatine",
        dosage="5g",
        reminder_time=time(14, 0),
        notes=None,
        is_active=True,
    )

    service.delete_supplement(supplement)

    repository.delete.assert_called_once_with(supplement)