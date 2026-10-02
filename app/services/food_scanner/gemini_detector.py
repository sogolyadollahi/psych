import json
import logging
from io import BytesIO

from google import genai
from google.genai import types
from PIL import Image
from pydantic import BaseModel

from app.core.config import settings
from app.services.food_scanner.detector import FoodDetector

logger = logging.getLogger(__name__)


class FoodDetectionError(Exception):
    """Raised when AI food detection fails."""

    pass


class DetectedFood(BaseModel):
    name: str


class FoodDetectionResponse(BaseModel):
    foods: list[DetectedFood]


class GeminiFoodDetector(FoodDetector):
    """
    Detect food names from an image using Google Gemini.

    This detector is responsible only for:

        image -> food names

    It does NOT:
        - search USDA
        - select FDC IDs
        - calculate nutrition
        - create MealItems
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = model or settings.AI_MODEL

        if not self.api_key:
            raise FoodDetectionError(
                "Gemini API key is not configured."
            )

        self.client = genai.Client(api_key=self.api_key)

    def detect(self, image: bytes) -> list[str]:
        """
        Detect visible food items from an image.

        Returns:
            list[str]: Detected food names.
        """

        if not image:
            raise FoodDetectionError(
                "Image cannot be empty."
            )

        try:
            # Validate image before sending it to Gemini.
            self._validate_image(image)

            mime_type = self._get_mime_type(image)

            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Part.from_bytes(
                        data=image,
                        mime_type=mime_type,
                    ),
                    (
                        "Identify the food items visibly present "
                        "in this image. "
                        "Return only foods that are clearly visible. "
                        "Use common, specific food names. "
                        "Do not guess nutrition, calories, quantities, "
                        "or USDA food IDs."
                    ),
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=FoodDetectionResponse.model_json_schema(),
                ),
            )

            if not response.text:
                raise FoodDetectionError(
                    "Gemini returned an empty response."
                )

            # Gemini returns JSON text.
            data = json.loads(response.text)

            # Validate Gemini's response with Pydantic.
            parsed = FoodDetectionResponse.model_validate(data)

            foods = [
                food.name.strip()
                for food in parsed.foods
                if food.name.strip()
            ]

            if not foods:
                raise FoodDetectionError(
                    "No food items were detected."
                )

            return foods

        except FoodDetectionError:
            raise

        except json.JSONDecodeError as exc:
            logger.warning(
                "Gemini returned invalid JSON: %s",
                exc,
            )
            raise FoodDetectionError(
                "Gemini returned invalid JSON."
            ) from exc

        except Exception as exc:
            logger.exception(
                "Gemini food detection failed"
            )

            raise FoodDetectionError(
                "Food detection service failed."
            ) from exc

    @staticmethod
    def _validate_image(image: bytes) -> None:
        """
        Validate that the provided bytes represent a readable image.
        """

        try:
            with Image.open(BytesIO(image)) as pil_image:
                pil_image.verify()

        except Exception as exc:
            raise FoodDetectionError(
                "Unable to process image."
            ) from exc

    @staticmethod
    def _get_mime_type(image: bytes) -> str:
        """
        Determine the MIME type of the image.
        """

        try:
            with Image.open(BytesIO(image)) as pil_image:
                image_format = pil_image.format

        except Exception as exc:
            raise FoodDetectionError(
                "Unable to determine image format."
            ) from exc

        mime_types = {
            "JPEG": "image/jpeg",
            "PNG": "image/png",
            "WEBP": "image/webp",
            "GIF": "image/gif",
        }

        mime_type = mime_types.get(image_format)

        if mime_type is None:
            raise FoodDetectionError(
                f"Unsupported image format: {image_format}"
            )

        return mime_type