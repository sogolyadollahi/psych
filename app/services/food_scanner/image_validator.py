from io import BytesIO

from PIL import Image


class ImageValidationError(ValueError):
    """Raised when an uploaded image is invalid."""


class ImageValidator:
    ALLOWED_MIME_TYPES = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    ALLOWED_FORMATS = {
        "JPEG",
        "PNG",
        "WEBP",
    }

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

    @classmethod
    def validate(
        cls,
        image: bytes,
        content_type: str | None = None,
    ) -> None:
        cls._validate_size(image)
        cls._validate_content_type(content_type)
        cls._validate_image(image)

    @classmethod
    def _validate_size(cls, image: bytes) -> None:
        if not image:
            raise ImageValidationError(
                "Image file is empty."
            )

        if len(image) > cls.MAX_FILE_SIZE:
            raise ImageValidationError(
                "Image file is too large. Maximum size is 5 MB."
            )

    @classmethod
    def _validate_content_type(
        cls,
        content_type: str | None,
    ) -> None:
        if content_type not in cls.ALLOWED_MIME_TYPES:
            raise ImageValidationError(
                "Unsupported image type."
            )

    @classmethod
    def _validate_image(cls, image: bytes) -> None:
        try:
            with Image.open(BytesIO(image)) as img:
                image_format = img.format

                if image_format not in cls.ALLOWED_FORMATS:
                    raise ImageValidationError(
                        "Unsupported image format."
                    )

                img.verify()

        except ImageValidationError:
            raise

        except Exception as exc:
            raise ImageValidationError(
                "Invalid or corrupted image."
            ) from exc