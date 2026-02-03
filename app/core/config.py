from pathlib import Path
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"] = "DEV"
    APP_NAME: str = "App"
    LOG_LEVEL: str = "INFO"

    # Основная ссылка для подключения
    DATABASE_URL: str = ""
    TEST_DATABASE_URL: str = ""

    # Эти поля можно оставить опциональными, так как в Docker
    # мы теперь используем готовую DATABASE_URL
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_PORT: Optional[str] = None

    SECRET_KEY: str = ""
    ALGORITHM: str = ""

    SENTRY_DSN: Optional[str] = None
    LOKI_URL: Optional[str] = None
    REDIS_URL: str = "redis://redis:6379/0"

    model_config = SettingsConfigDict(
        # Pydantic сначала посмотрит в системные переменные (из docker-compose),
        # а если их нет — пойдет искать файлы по списку.
        env_file=(BASE_DIR / ".env", BASE_DIR / ".docker.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
