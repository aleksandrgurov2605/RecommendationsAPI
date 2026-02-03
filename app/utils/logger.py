import logging
import sys

import logging_loki  # pip install python-logging-loki-v2

from app.core.config import settings

logger = logging.getLogger("rec-shop")
logger.setLevel(settings.LOG_LEVEL)

log_format = (
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]"
)
formatter = logging.Formatter(log_format)

# Вывод в консоль (STDOUT)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Отправка в Loki через v2
if settings.LOKI_URL and settings.MODE != "TEST":
    try:
        import logging_loki

        loki_handler = logging_loki.LokiHandler(
            url=settings.LOKI_URL,
            tags={"app_name": settings.APP_NAME, "env": settings.MODE},
            version="1",
        )
        loki_handler.setFormatter(formatter)
        logger.addHandler(loki_handler)
    except Exception as e:
        print(f"Loki initialization failed: {e}")
