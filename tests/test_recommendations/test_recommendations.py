import logging

import pytest
from sqlalchemy import select

from app.models import Recommendation
from app.services.recommendations import RecommendationService
from app.utils.unitofwork import UnitOfWork


@pytest.mark.asyncio
async def test_generate_recommendations_api(client, mock_recommendation_task):
    """Проверка роута: задача должна улетать в Celery."""
    resp = await client.post(
        "/recommendations/generate", json={"user_id": 1, "min_pair_count": 1}
    )
    assert resp.status_code == 200
    assert resp.json()["task_id"] == "fake-task-id-123"
    mock_recommendation_task.assert_called_once()


@pytest.mark.asyncio
async def test_recommendation_logic_integration(
    session_factory, setup_complex_purchases
):
    """Проверка полной логики генерации и сохранения."""
    uow = UnitOfWork()
    uow.session_factory = session_factory
    user_id = setup_complex_purchases["user_id"]
    target_id = setup_complex_purchases["target_item_id"]

    # Исправлено: запуск внутри контекста UOW
    async with uow:
        await RecommendationService.generate_recommendations(
            uow, user_id=user_id, min_pair_count=1
        )

    async with session_factory() as session:
        res = await session.execute(select(Recommendation).filter_by(user_id=user_id))
        rec = res.scalar_one_or_none()
        assert rec is not None
        assert rec.item_id == target_id


@pytest.mark.asyncio
async def test_recommendation_update_existing(session_factory, setup_complex_purchases):
    """Проверка обновления существующей рекомендации."""
    uow = UnitOfWork()
    uow.session_factory = session_factory
    user_id = setup_complex_purchases["user_id"]

    async with session_factory() as session:
        session.add(Recommendation(user_id=user_id, item_id=999))
        await session.commit()

    async with uow:
        await RecommendationService.generate_recommendations(
            uow, user_id=user_id, min_pair_count=1
        )

    async with session_factory() as session:
        res = await session.execute(select(Recommendation).filter_by(user_id=user_id))
        rec = res.scalar_one()
        assert rec.item_id == setup_complex_purchases["target_item_id"]


@pytest.mark.asyncio
async def test_generate_recommendations_no_history(session_factory):
    """Если покупок нет — рекомендация не создается."""
    uow = UnitOfWork()
    uow.session_factory = session_factory
    user_id = 888  # Пользователь без истории

    async with uow:
        await RecommendationService.generate_recommendations(
            uow, user_id=user_id, min_pair_count=1
        )

    async with session_factory() as session:
        res = await session.execute(select(Recommendation).filter_by(user_id=user_id))
        assert res.scalar_one_or_none() is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "min_pair, should_find",
    [
        (1, True),
        (5, False),  # У нас в фикстуре всего 1 совпадение, так что при 5 не найдет
    ],
)
async def test_recommendation_threshold(
    session_factory, setup_complex_purchases, min_pair, should_find
):
    uow = UnitOfWork()
    uow.session_factory = session_factory
    user_id = setup_complex_purchases["user_id"]

    async with uow:
        await RecommendationService.generate_recommendations(
            uow, user_id=user_id, min_pair_count=min_pair
        )

    async with session_factory() as session:
        res = await session.execute(select(Recommendation).filter_by(user_id=user_id))
        rec = res.scalar_one_or_none()
        assert (rec is not None) is should_find


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id, expected_status",
    [
        ("abc", 422),
        (None, 422),
        (-1, 422),
    ],
)
async def test_get_recommendations_validation(client, user_id, expected_status):
    """Проверка валидации Query-параметров в GET /recommendations/"""
    params = {"user_id": user_id} if user_id is not None else {}
    response = await client.get("/recommendations/", params=params)
    assert response.status_code == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"user_id": -5, "min_pair_count": 1}, 422),  # Отрицательный ID (gt=0 в схеме)
        ({"user_id": 1, "min_pair_count": 0}, 422),  # Невалидный порог (gt=0 в схеме)
        ({"user_id": 1}, 200),  # Ок, min_pair_count имеет дефолт
        ({}, 422),  # Пустое тело
    ],
)
async def test_generate_recommendations_schema_validation(
    client, mock_recommendation_task, payload, expected_status
):
    """Проверка валидации Pydantic-схемы RecommendationCreate в POST /generate"""
    response = await client.post("/recommendations/generate", json=payload)
    assert response.status_code == expected_status



