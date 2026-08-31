from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db
from app.repositories.supplement_repository import SupplementRepository
from app.services.supplement_service import SupplementService


def get_supplement_repository(
    db: Session = Depends(get_db),
) -> SupplementRepository:

    return SupplementRepository(db)


def get_supplement_service(
    repository: SupplementRepository = Depends(
        get_supplement_repository
    ),
) -> SupplementService:

    return SupplementService(repository)