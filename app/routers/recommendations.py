from fastapi import APIRouter, Query

from app.dependencies.dependencies import UOWDep
from app.schemas.recommendations import RecommendationCreate

from app.services.recommendations import RecommendationService
from app.utils.logger import logger


router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"]
)


@router.get("/")
async def get_recommendations(
        uow: UOWDep,
        user_id: int = Query(..., gt=0),
):
    logger.info(f"Получение рекомендаций для пользователя {user_id}")
    result = await RecommendationService.get_recommendations(uow, user_id)
    return {"recommendations": result}


@router.post("/generate")
async def generate_recommendations(
        recommendation: RecommendationCreate
):
    logger.info(f"Старт генерации рекомендаций для пользователя {recommendation.user_id}")
    from app.utils.celery_tasks import generate_recommendations_task
    logger.info("Импорт задачи выполнен успешно")
    task = generate_recommendations_task.delay(
        recommendation.user_id,
        recommendation.min_pair_count
    )
    logger.info(f"Успех! ID: {task.id}")
    return {
        "result": f"recommendation generation started",
        "task_id": task.id,
        "status": "queued"
    }


# @router.get("/status/{task_id}")
# async def get_task_status(task_id: str):
#     # Получаем объект задачи по ID
#     task_result = AsyncResult(task_id, app=celery_app)
#
#     result = {
#         "task_id": task_id,
#         "status": task_result.status,  # PENDING, STARTED, SUCCESS, FAILURE
#     }
#
#     if task_result.status == 'SUCCESS':
#         result["message"] = "Расчет окончен"
#     elif task_result.status == 'FAILURE':
#         result["error"] = str(task_result.result)
#
#     return result