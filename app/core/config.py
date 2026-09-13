from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # -------------------------
    # Application
    # -------------------------
    APP_NAME: str = "Psych"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # -------------------------
    # Security
    # -------------------------
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # -------------------------
    # Database
    # -------------------------
    DATABASE_URL: str

    # -------------------------
    # Uploads
    # -------------------------
    UPLOAD_DIR: str = "uploads"

    # -------------------------
    # AI
    # -------------------------
    AI_PROVIDER: str = "ollama"
    AI_MODEL: str = "gemma3:4b"

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # Gemini
    GEMINI_API_KEY: str = ""

    # -------------------------
    # Nutrition / USDA
    # -------------------------
    USDA_API_KEY: str = ""
    USDA_API_BASE_URL: str = "https://api.nal.usda.gov/fdc/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()