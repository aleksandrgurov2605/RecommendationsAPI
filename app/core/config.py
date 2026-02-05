from pathlib import Path
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"] = "DEV"
    APP_NAME: str = "App"
    LOG_LEVEL: str = "INFO"

    DATABASE_URL: str = ""
    TEST_DATABASE_URL: str = ""

    POSTGRES_DB: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_PORT: Optional[str] = None

    SECRET_KEY: str = ""
    ALGORITHM: str = ""

    SENTRY_DSN: Optional[str] = None
    LOKI_URL: Optional[str] = None
    REDIS_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env", BASE_DIR / ".docker.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
