import pytest


@pytest.mark.asyncio
async def test_cart_workflow(client, setup_cart_db, cart_auth_headers):
    item1_id = setup_cart_db["item1"].id

    # 1. Добавляем товар в корзину
    add_resp = await client.post(
        "/cart/units",
        json={"item_id": item1_id, "quantity": 2},
        headers=cart_auth_headers,
    )
    assert add_resp.status_code == 201
    assert add_resp.json()["quantity"] == 2

    # 2. Получаем корзину
    get_resp = await client.get("/cart/", headers=cart_auth_headers)
    assert get_resp.status_code == 200
    assert len(get_resp.json()["units"]) == 1
    assert get_resp.json()["units"][0]["item"]["id"] == item1_id

    # 3. Обновляем количество
    update_resp = await client.put(
        f"/cart/units/{item1_id}",
        json={"item_id": item1_id, "quantity": 5},
        headers=cart_auth_headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["quantity"] == 5

    # 4. Удаляем один товар
    item_id = add_resp.json()["item"]["id"]
    del_unit_resp = await client.delete(
        f"/cart/units/{item_id}", headers=cart_auth_headers
    )
    assert del_unit_resp.status_code == 204


@pytest.mark.asyncio
async def test_clear_cart(client, setup_cart_db, cart_auth_headers):
    # Сначала добавим товар
    await client.post(
        "/cart/units",
        json={"item_id": setup_cart_db["item1"].id, "quantity": 1},
        headers=cart_auth_headers,
    )

    # Полная очистка
    r = await client.delete("/cart/", headers=cart_auth_headers)
    assert r.status_code == 204

    # Проверка, что пусто
    check = await client.get("/cart/", headers=cart_auth_headers)
    assert len(check.json()["units"]) == 0


@pytest.mark.asyncio
async def test_cart_unauthorized(client):
    # Проверка защиты
    r = await client.get("/cart/")
    assert r.status_code == 401
