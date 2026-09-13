import base64
import json
from typing import Any

import httpx

from app.core.config import settings
from app.services.food_scanner.detector import FoodDetector


class FoodDetectionError(Exception):
    """Raised when the AI food detection service fails."""


class OllamaFoodDetector(FoodDetector):
    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float = 600.0,
    ):
        self.base_url = (
            base_url or settings.OLLAMA_BASE_URL
        ).rstrip("/")

        self.model = (
            model or settings.AI_MODEL
        )

        self.timeout = timeout

    def detect(self, image: bytes) -> list[str]:
        if not image:
            raise FoodDetectionError(
                "Image cannot be empty."
            )

        image_base64 = base64.b64encode(image).decode("utf-8")

        prompt = """
Identify the food items clearly visible in this image.

Return ONLY valid JSON in exactly this format:

{
  "foods": [
    "food name 1",
    "food name 2"
  ]
}

Rules:
- Return only clearly visible food items.
- Do not estimate calories or nutrition.
- Do not return USDA FDC IDs.
- Do not return explanations.
- Use concise, common food names.
- Do not include plates, utensils, tables, or other non-food objects.
- If no food is clearly visible, return:
  {"foods": []}
"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [image_base64],
            "stream": False,
            "format": "json",
        }

        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

        except httpx.HTTPError as exc:
            raise FoodDetectionError(
                "Ollama food detection service is unavailable."
            ) from exc

        try:
            response_data = response.json()

        except ValueError as exc:
            raise FoodDetectionError(
                "Ollama returned an invalid response."
            ) from exc

        raw_response = response_data.get("response")

        if not isinstance(raw_response, str):
            raise FoodDetectionError(
                "Ollama response is missing the detection result."
            )

        return self._parse_foods(raw_response)

    @staticmethod
    def _parse_foods(
        raw_response: str,
    ) -> list[str]:

        try:
            parsed: Any = json.loads(raw_response)

        except json.JSONDecodeError as exc:
            raise FoodDetectionError(
                "AI returned malformed JSON."
            ) from exc

        if not isinstance(parsed, dict):
            raise FoodDetectionError(
                "AI response must be a JSON object."
            )

        foods = parsed.get("foods")

        if not isinstance(foods, list):
            raise FoodDetectionError(
                "AI response must contain a 'foods' list."
            )

        cleaned_foods: list[str] = []

        for food in foods:

            if not isinstance(food, str):
                raise FoodDetectionError(
                    "AI food names must be strings."
                )

            food = food.strip()

            if food:
                cleaned_foods.append(food)

        return cleaned_foods