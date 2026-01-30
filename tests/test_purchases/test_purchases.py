import pytest
from sqlalchemy import select
from app.models.items import Item



@pytest.mark.asyncio
@pytest.mark.parametrize("item_key, quantity_to_buy, expected_stock_after, expected_status", [
    ("item1", 1, 9, 200),
    ("item1", 10, 0, 200),
    ("item1", 11, 10, 409),
],
                         ids=[
                             "success",
                             "success_all",
                             "unsuccess_NotEnoughItemsError",
                         ])
async def test_checkout_parametrized(
        client,
        setup_purchase_data,
        purchase_auth_headers,
        session_factory,
        item_key,
        quantity_to_buy,
        expected_stock_after,
        expected_status
):
    """
    Тест успешного и неуспешного оформления заказа с проверкой остатков с помощью parametrize.
    """
    item = setup_purchase_data[item_key]
    item_id = item.id

    # 1. Добавляем товар в корзину
    await client.post(
        "/cart/units",
        json={"item_id": item_id, "quantity": quantity_to_buy},
        headers=purchase_auth_headers
    )

    # 2. Оформляем заказ
    response = await client.get("/purchases/checkout", headers=purchase_auth_headers)
    assert response.status_code == expected_status

    # 3. Проверяем остаток в базе данных
    async with session_factory() as session:
        query = select(Item).filter_by(id=item_id)
        result = await session.execute(query)
        updated_item = result.scalar_one()

        assert updated_item.stock == expected_stock_after


@pytest.mark.asyncio
async def test_checkout_atomicity_failure(client, setup_purchase_data, purchase_auth_headers, session_factory):
    """
    Тест атомарности: если один товар недоступен, весь заказ отменяется.
    """
    item1 = setup_purchase_data["item1"]  # Stock = 10
    item2 = setup_purchase_data["item2"]  # Stock = 10

    # Добавляем доступный товар
    await client.post(
        "/cart/units",
        json={"item_id": item1.id, "quantity": 5},
        headers=purchase_auth_headers
    )
    # Добавляем недоступный товар (больше, чем есть)
    await client.post(
        "/cart/units",
        json={"item_id": item2.id, "quantity": 15},
        headers=purchase_auth_headers
    )

    # Пытаемся оформить заказ - ожидаем ошибку
    response = await client.get("/purchases/checkout", headers=purchase_auth_headers)
    assert response.status_code == 409
    assert "stock" in response.json()["detail"].lower()

    # Проверяем, что остатки обоих товаров НЕ изменились
    async with session_factory() as session:
        item1_db = (await session.execute(select(Item).filter_by(id=item1.id))).scalar_one()
        item2_db = (await session.execute(select(Item).filter_by(id=item2.id))).scalar_one()

        assert item1_db.stock == 10
        assert item2_db.stock == 10


@pytest.mark.asyncio
async def test_get_purchases_list(client, purchase_auth_headers):
    response = await client.get("/purchases/", headers=purchase_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "purchases" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_get_purchase_by_id(client, setup_purchase_data, purchase_auth_headers):
    await client.post(
        "/cart/units",
        json={"item_id": setup_purchase_data["item1"].id, "quantity": 1},
        headers=purchase_auth_headers
    )
    order_data = (await client.get("/purchases/checkout", headers=purchase_auth_headers)).json()
    p_id = order_data["id"]

    # Проверяем эндпоинт
    response = await client.get(f"/purchases/{p_id}", headers=purchase_auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == p_id
