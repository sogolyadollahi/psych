from decimal import Decimal

import httpx
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.meal_item_repository import MealItemRepository
from app.repositories.meal_repository import MealRepository
from app.schemas.food_scanner import (
    FoodCandidate,
    FoodCandidateResponse,
    FoodScanItemCreate,
    FoodScanResponse,
)
from app.schemas.meal import MealItemResponse
from app.services.food_scanner.detector import FoodDetector
from app.services.food_scanner.image_validator import (
    ImageValidationError,
    ImageValidator,
)
from app.services.food_scanner.mock_detector import MockFoodDetector
from app.services.food_scanner.scanner_service import ScannerService
from app.services.meal_item_service import MealItemService
from app.services.nutrition.nutrition_service import NutritionService
from app.services.nutrition.usda_provider import USDAProvider


router = APIRouter(
    prefix="/food-scanner",
    tags=["Food Scanner"],
)


def get_scanner_service(
    db: Session,
) -> ScannerService:
    """
    Build and return ScannerService with its dependencies.

    Currently MockFoodDetector is used for AI food detection.
    It will later be replaced by the real AI detector.
    """

    detector: FoodDetector = MockFoodDetector()

    provider = USDAProvider()

    nutrition_service = NutritionService(
        provider=provider,
    )

    meal_repository = MealRepository(db)

    meal_item_repository = MealItemRepository(db)

    meal_item_service = MealItemService(
        meal_item_repository=meal_item_repository,
        meal_repository=meal_repository,
    )

    return ScannerService(
        detector=detector,
        nutrition_service=nutrition_service,
        meal_item_service=meal_item_service,
    )


@router.post(
    "/scan",
    response_model=FoodScanResponse,
    status_code=status.HTTP_200_OK,
)
async def scan_food(
    image: UploadFile = File(...),
) -> FoodScanResponse:
    """
    Validate an uploaded food image and detect food names.

    Currently uses MockFoodDetector.
    """

    image_bytes = await image.read()

    try:
        ImageValidator.validate(
            image=image_bytes,
            content_type=image.content_type,
        )
    except ImageValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    detector: FoodDetector = MockFoodDetector()

    detections = detector.detect(
        image_bytes,
    )

    return FoodScanResponse(
        detections=[
            {"name": name}
            for name in detections
        ]
    )


@router.get(
    "/candidates",
    response_model=FoodCandidateResponse,
)
def get_food_candidates(
    detected_food: str,
    page_size: int = 10,
    db: Session = Depends(get_db),
) -> FoodCandidateResponse:
    """
    Search USDA for foods matching the detected food name.
    """

    if not detected_food.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Detected food cannot be empty.",
        )

    if page_size < 1 or page_size > 50:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="page_size must be between 1 and 50.",
        )

    scanner_service = get_scanner_service(db)

    try:
        candidates = scanner_service.find_candidates(
            detected_food=detected_food,
            page_size=page_size,
        )
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Food database service is currently unavailable.",
        ) from exc

    return FoodCandidateResponse(
        detected_food=detected_food,
        candidates=[
            FoodCandidate(**candidate)
            for candidate in candidates
        ],
    )


@router.post(
    "/items",
    response_model=MealItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_scanned_food_item(
    data: FoodScanItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MealItemResponse:
    """
    Create a MealItem using a user-selected USDA food
    and the provided quantity in grams.
    """

    scanner_service = get_scanner_service(db)

    try:
        item = scanner_service.create_meal_item_from_food(
            meal_id=data.meal_id,
            user_id=current_user.id,
            fdc_id=data.fdc_id,
            quantity_grams=data.quantity_grams,
        )
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Food database service is currently unavailable.",
        ) from exc

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found or does not belong to the current user.",
        )

    return MealItemResponse.model_validate(
        item,
        from_attributes=True,
    )