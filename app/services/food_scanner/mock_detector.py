from app.services.food_scanner.detector import FoodDetector


class MockFoodDetector(FoodDetector):
    def detect(self, image: bytes) -> list[str]:
        return [
            "grilled chicken breast",
            "white rice",
            "salad",
        ]