import logging
from logging.handlers import RotatingFileHandler

from app.core.config import settings

logger = logging.getLogger("My shop")
logger.setLevel(settings.LOG_LEVEL)

file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]"
)
console_formatter = logging.Formatter("%(levelname)s:     %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

file_handler = RotatingFileHandler(
    "app.log", maxBytes=10**7, backupCount=5, encoding="utf-8"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
