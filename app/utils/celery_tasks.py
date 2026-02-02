import asyncio

import sentry_sdk
from celery import Celery
from celery.signals import worker_process_init
from sentry_sdk.integrations.celery import CeleryIntegration

from app.core.config import settings
from app.services.recommendations import RecommendationService
from app.utils.logger import logger


@worker_process_init.connect
def init_sentry(**kwargs):
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            integrations=[
                CeleryIntegration(),
            ],
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
            environment=settings.MODE,
        )


celery_app = Celery(
    "tasks", broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/0"
)


@celery_app.task(name="generate_recommendations_task")
def generate_recommendations_task(user_id: int, min_pair_count: int):
    async def run_process():
        from app.utils.unitofwork import UnitOfWork

        async with UnitOfWork() as uow:
            await RecommendationService.generate_recommendations(
                uow, user_id, min_pair_count
            )

    try:
        asyncio.run(run_process())
    except Exception as e:
        logger.error(f"Task Error: {e}")


# uv run celery -A app.utils.celery_tasks.celery_app worker --loglevel=debug
# uv run celery -A app.utils.celery_tasks.celery_app worker --loglevel=debug -P eventlet
# uv run celery -A app.utils.celery_tasks.celery_app worker --loglevel=info -P solo
