import random

import pytest
import pytest_asyncio
from unittest.mock import MagicMock
from app.models import Recommendation, Item, User, Purchase, PurchaseUnit, Category
from app.utils.security import get_password_hash


@pytest.fixture
def mock_recommendation_task(mocker):
    """Изолируем Celery."""
    mock_task = MagicMock()
    mock_task.id = "fake-task-id-123"
    # Путь должен совпадать с тем, где импортируется задача в роуте
    return mocker.patch("app.utils.celery_tasks.generate_recommendations_task.delay", return_value=mock_task)


@pytest_asyncio.fixture
async def setup_complex_purchases(session_factory):
    """
    Создает матрицу покупок для теста алгоритма:
    User 1 купил: Item A
    User 2 купил: Item A + Item B (связка для рекомендации)
    Результат для User 1: должен получить рекомендацию Item B
    """
    async with session_factory() as session:
        cat = Category(name="Electronics")
        session.add(cat)
        await session.flush()
        u1 = User(email="u1@t.com", name="User1",  password=get_password_hash("password"), is_active=True)
        u2 = User(email="u2@t.com", name="User2",  password=get_password_hash("password"), is_active=True)
        ia = Item(name="Item A", price=100, category_id=cat.id, stock=10,
                  is_active=True, description="Test Item A description")
        ib = Item(name="Item B", price=200, category_id=cat.id,
                  stock=10, is_active=True, description="Test Item B description")
        session.add_all([u1, u2, ia, ib])
        await session.flush()

        # Покупка User 2 (связывает A и B)
        p2 = Purchase(user_id=u2.id, status="completed", total_amount=300)
        session.add(p2)
        await session.flush()
        session.add_all([
            PurchaseUnit(purchase_id=p2.id, item_id=ia.id, quantity=1, unit_price=100, total_price=100),
            PurchaseUnit(purchase_id=p2.id, item_id=ib.id, quantity=1, unit_price=200, total_price=200)
        ])

        # Покупка User 1 (только A)
        p1 = Purchase(user_id=u1.id, status="completed", total_amount=100)
        session.add(p1)
        await session.flush()
        session.add(PurchaseUnit(purchase_id=p1.id, item_id=ia.id, quantity=1, unit_price=100, total_price=100))

        await session.commit()
        return {"user_id": u1.id, "target_item_id": ib.id}


# @pytest_asyncio.fixture
# async def setup_mass_data(session_factory):
#     """
#     Генерирует 100+ транзакций для проверки производительности SQL.
#     Создает явную закономерность: те, кто покупает Item 1, почти всегда покупают Item 2.
#     """
#     async with session_factory() as session:
#         # Создаем 20 пользователей и 50 товаров
#         users = [User(email=f"u{i}@t.com", hashed_password="1", is_active=True) for i in range(20)]
#         items = [Item(name=f"Item {i}", price=100, stock=1000, is_active=True) for i in range(50)]
#         session.add_all(users + items)
#         await session.flush()
#
#         # Создаем 100 покупок
#         for i in range(100):
#             buyer = random.choice(users)
#             p = Purchase(user_id=buyer.id, status="completed", total_amount=0)
#             session.add(p)
#             await session.flush()
#
#             # Генерируем "сигнал": если это четная покупка, берем Item 0 и Item 1 вместе
#             if i % 2 == 0:
#                 chosen_items = [items[0], items[1]]
#             else:
#                 chosen_items = random.sample(items[2:], k=2)  # Остальное - шум
#
#             for itm in chosen_items:
#                 session.add(PurchaseUnit(
#                     purchase_id=p.id, item_id=itm.id,
#                     quantity=1, unit_price=itm.price, total_price=itm.price
#                 ))
#
#         await session.commit()
#         # Возвращаем ID пользователя, который купил только Item 0
#         target_user = users[0]
#         # Очистим его историю и дадим только Item 0
#         return {"user_id": target_user.id, "expected_item_id": items[1].id, "item_zero_id": items[0].id}
