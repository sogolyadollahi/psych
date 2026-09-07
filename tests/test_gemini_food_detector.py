from pathlib import Path

from app.services.food_scanner.gemini_detector import (
    FoodDetectionError,
    GeminiFoodDetector,
)


IMAGE_PATH = Path("tests/assets/food_test.jpg")


def main() -> None:
    if not IMAGE_PATH.exists():
        print(f"Image not found: {IMAGE_PATH}")
        return

    image = IMAGE_PATH.read_bytes()

    try:
        detector = GeminiFoodDetector()

        foods = detector.detect(image)

        print("\nDetected foods:")

        for food in foods:
            print(f"- {food}")

        print("\nGemini food detection: OK")

    except FoodDetectionError as exc:
        print(f"\nFood detection failed: {exc}")


if __name__ == "__main__":
    main()