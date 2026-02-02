from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"] = "DEV"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    DATABASE_URL: str = ""
    TEST_DATABASE_URL: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_HOST: str = ""
    POSTGRES_PORT: str = ""

    SECRET_KEY: str = ""
    ALGORITHM: str = ""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env" if MODE == "DEV" else BASE_DIR / ".docker.env",
        extra="ignore",
    )


settings = Settings()
