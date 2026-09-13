from pathlib import Path

import ollama


IMAGE_PATH = Path("tests/assets/food_test.jpg")
MODEL = "llama3.2-vision"


def main() -> None:
    if not IMAGE_PATH.exists():
        print(f"Image not found: {IMAGE_PATH}")
        return

    image = IMAGE_PATH.read_bytes()

    print("Sending image to Ollama...")
    print(f"Model: {MODEL}")

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": (
                    "Identify the food items clearly visible in this image. "
                    "Return only the food names, one per line. "
                    "Do not provide calories, nutrition, quantities, "
                    "or USDA IDs. "
                    "Do not identify objects that are not food."
                ),
                "images": [image],
            }
        ],
    )

    content = response["message"]["content"]

    print("\nOllama response:")
    print(content)

    print("\nOllama Vision test: OK")


if __name__ == "__main__":
    main()