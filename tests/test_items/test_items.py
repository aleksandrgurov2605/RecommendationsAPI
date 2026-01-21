import pytest


@pytest.mark.parametrize(
    "data, expected_status",
    [
        ({"name": "Item_1", "description": "description", "price": 10, "stock": 10, "category_id": 1}, 201),
        ({"name": "Item_2", "description": "description", "price": 10, "stock": 10, "category_id": 1}, 201),
        ({"name": "Item_3", "description": "description", "price": 10, "stock": 10, "category_id": 1}, 201),
        ({"name": "Item_4", "description": "description", "price": 10, "stock": 10, "category_id": 10}, 422),
        ({"name": "", "description": "description", "price": 10, "stock": 10, "category_id": 1}, 422),
        ({"name": "6", "description": "description", "price": 10, "stock": 10, "category_id": 1}, 422),
        ({"name": "Item_7", "description": "description", "price": 0, "stock": 10, "category_id": 1}, 422),
        ({"name": "Item_7", "description": "description", "price": -1, "stock": 10, "category_id": 1}, 422),
        ({"name": "Item_8", "description": "description", "price": 10, "stock": 0, "category_id": 1}, 201),
        ({"name": "Item_9", "description": "description", "price": 10, "stock": -10, "category_id": 1}, 422),
    ],
    ids=[
        "success",
        "success",
        "success",
        "unsuccess non_existent_category",
        "unsuccess empty_name",
        "unsuccess name_too_short",
        "unsuccess zero price",
        "unsuccess negative price",
        "success zero stock",
        "unsuccess negative stock",
    ]
)
@pytest.mark.asyncio
async def test_create_item(client, setup_database, data, expected_status):
    r = await client.post(
        "/items/",
        json=data,
    )
    assert r.status_code == expected_status


@pytest.mark.asyncio
async def test_get_all_items(client, setup_database):
    items_from_db = await client.get("/items/")
    assert items_from_db.status_code == 200
    assert len(items_from_db.json()) == 2
    assert items_from_db.json()[0]["name"] == "iPhone 17"
    assert items_from_db.json()[1]["name"] == "Galaxy S25 Ultra"


@pytest.mark.parametrize(
    "item_id, expected_status, expected_name",
    [
        (1, 200, "iPhone 17"),
        (999, 404, None),
    ],
    ids=[
        "success",
        "wrong ID"
    ]
)
@pytest.mark.asyncio
async def test_get_item_by_id(client, setup_database, item_id, expected_status, expected_name):
    r = await client.get(f"/items/{item_id}")
    assert r.status_code == expected_status
    if expected_status == 200:
        assert r.json()["name"] == expected_name


@pytest.mark.parametrize(
    "item_id, update_data, expected_status",
    [
        (1, {"name": "iPhone 17", "description": "new_description", "price": 799, "stock": 9, "category_id": 2}, 200),
        (2, {"name": "Galaxy S25", "description": "The Samsung", "price": 799, "stock": 9, "category_id": 2}, 200),
        (999, {"name": "Galaxy S25", "description": "The Samsung", "price": 799, "stock": 9, "category_id": 2}, 404),
        (2, {"name": "Galaxy S25", "description": "The Samsung", "price": 799, "stock": 9, "category_id": 999}, 422),
        (1, {"name": "17", "description": "iPhone", "price": 799, "stock": 9, "category_id": 2}, 422),
        (1, {"name": "Galaxy S25", "description": "The Samsung", "price": 0, "stock": 9, "category_id": 2}, 422),
        (2, {"name": "Galaxy S25", "description": "The Samsung", "price": -799, "stock": 9, "category_id": 2}, 422),
        (2, {"name": "Galaxy S25", "description": "The Samsung", "price": 799, "stock": 0, "category_id": 2}, 200),
        (1, {"name": "17", "description": "iPhone", "price": 799, "stock": -9, "category_id": 2}, 422),
    ],
    ids=[
        "success",
        "success",
        "item not found",
        "wrong category",
        "name_too_short",
        "unsuccess zero price",
        "unsuccess negative price",
        "success zero stock",
        "unsuccess negative stock",
    ]
)
@pytest.mark.asyncio
async def test_update_item(client, setup_database, item_id, update_data, expected_status):
    r = await client.put(f"/items/{item_id}", json=update_data)
    assert r.status_code == expected_status
    if expected_status == 200:
        assert r.json()["name"] == update_data["name"]


@pytest.mark.parametrize(
    "item_id, expected_status",
    [
        (1, 204),
        (999, 404),
    ],
    ids=[
        "success",
        "item not found"
    ]
)
@pytest.mark.asyncio
async def test_delete_item(client, setup_database, item_id, expected_status):
    # Удаление
    r = await client.delete(f"/items/{item_id}")
    assert r.status_code == expected_status

    # Проверка, что после 204 ресурс действительно пропал
    if expected_status == 204:
        check = await client.get(f"/items/{item_id}")
        assert check.status_code == 404
