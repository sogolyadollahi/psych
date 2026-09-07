import base64
from io import BytesIO

from openai import OpenAI
from PIL import Image
from pydantic import BaseModel

from app.core.config import settings
from app.services.food_scanner.detector import FoodDetector


class FoodDetectionError(Exception):
    """Raised when AI food detection fails."""

    pass


class DetectedFood(BaseModel):
    name: str


class FoodDetectionResponse(BaseModel):
    foods: list[DetectedFood]


class OpenAIFoodDetector(FoodDetector):
    """
    Detect food names from an image using OpenAI vision.

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
        self.api_key = api_key or settings.AI_API_KEY
        self.model = model or settings.AI_MODEL

        if not self.api_key:
            raise FoodDetectionError(
                "AI API key is not configured."
            )

        self.client = OpenAI(
            api_key=self.api_key,
        )

    def detect(
        self,
        image: bytes,
    ) -> list[str]:
        """
        Detect food names from the provided image.
        """

        if not image:
            raise FoodDetectionError(
                "Image cannot be empty."
            )

        try:
            image_data_url = self._build_image_data_url(
                image
            )

            response = self.client.responses.parse(
                model=self.model,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": (
                                    "Identify the food items visible "
                                    "in this image. "
                                    "Return only foods that are visibly "
                                    "present. "
                                    "Use common, specific food names. "
                                    "Do not guess nutrition, calories, "
                                    "quantities, or USDA IDs."
                                ),
                            },
                            {
                                "type": "input_image",
                                "image_url": image_data_url,
                            },
                        ],
                    }
                ],
                text_format=FoodDetectionResponse,
            )

            parsed = response.output_parsed

            if parsed is None:
                raise FoodDetectionError(
                    "AI returned no structured food detection result."
                )

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

        except Exception as exc:
            raise FoodDetectionError(
                "Food detection service failed."
            ) from exc

    @staticmethod
    def _build_image_data_url(
        image: bytes,
    ) -> str:
        """
        Convert image bytes to a base64 data URL.

        The MIME type is detected from the actual image format
        instead of trusting the upload filename.
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

        encoded_image = base64.b64encode(
            image
        ).decode("utf-8")

        return (
            f"data:{mime_type};base64,{encoded_image}"
        )