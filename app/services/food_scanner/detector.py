from abc import ABC, abstractmethod


class FoodDetector(ABC):
    @abstractmethod
    def detect(self, image: bytes) -> list[str]:
        """Detect food names from an image."""
        raise NotImplementedError