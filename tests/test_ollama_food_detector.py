from pathlib import Path

from app.services.food_scanner.ollama_detector import (
    FoodDetectionError,
    OllamaFoodDetector,
)


IMAGE_PATH = Path("tests/assets/food_test.jpg")


def main() -> None:
    if not IMAGE_PATH.exists():
        print(f"Image not found: {IMAGE_PATH}")
        return

    image = IMAGE_PATH.read_bytes()

    detector = OllamaFoodDetector()

    try:
        foods = detector.detect(image)

    except FoodDetectionError as exc:
        print(f"Food detection failed: {exc}")
        return

    print("Food detection successful!")
    print("Detected foods:")

    if not foods:
        print("No food detected.")
        return

    for index, food in enumerate(foods, start=1):
        print(f"{index}. {food}")


if __name__ == "__main__":
    main()