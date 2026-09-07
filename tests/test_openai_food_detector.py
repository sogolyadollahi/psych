from pathlib import Path
import traceback

from app.services.food_scanner.openai_detector import (
    FoodDetectionError,
    OpenAIFoodDetector,
)


IMAGE_PATH = Path("tests/assets/food_test.jpg")


def main() -> None:
    if not IMAGE_PATH.exists():
        print(f"Image not found: {IMAGE_PATH}")
        return

    image = IMAGE_PATH.read_bytes()

    try:
        detector = OpenAIFoodDetector()

        foods = detector.detect(image)

        print("\nDetected foods:")
        for food in foods:
            print(f"- {food}")

        print("\nOpenAI food detection: OK")

    except FoodDetectionError as exc:
        print(f"\nFood detection failed: {exc}")
        print("\nOriginal exception:")
        print(repr(exc.__cause__))

        print("\nFull traceback:")
        traceback.print_exception(
            type(exc),
            exc,
            exc.__traceback__,
        )


if __name__ == "__main__":
    main()