import pytest


@pytest.mark.parametrize(
    "data, expected_status",
    [
        ({"name": "First", "parent_id": None}, 201),
        ({"name": "Second", "parent_id": 1}, 201),
        ({"name": "Third", "parent_id": 2}, 201),
        ({"name": "Fourth", "parent_id": 10}, 400),
        ({"name": "", "parent_id": 1}, 422),
        ({"T": "", "parent_id": 1}, 422),
    ],
    ids=[
        "success",
        "success",
        "success",
        "non_existent_parent",
        "empty_name",
        "name_too_short"
    ]
)
@pytest.mark.asyncio
async def test_create_category(client, setup_database, data, expected_status):
    r = await client.post(
        "/categories/",
        json=data,
    )
    assert r.status_code == expected_status


@pytest.mark.asyncio
async def test_get_all_categories(client, setup_database):
    cats_from_db = await client.get("/categories/")
    assert cats_from_db.status_code == 200
    assert len(cats_from_db.json()) == 2
    assert cats_from_db.json()[0]["name"] == "Электроника"
    assert cats_from_db.json()[1]["name"] == "Смартфоны"


@pytest.mark.parametrize(
    "category_id, expected_status, expected_name",
    [
        (1, 200, "Электроника"),
        (999, 404, None),
    ],
    ids=[
        "success",
        "wrong ID"
    ]
)
@pytest.mark.asyncio
async def test_get_category_by_id(client, setup_database, category_id, expected_status, expected_name):
    r = await client.get(f"/categories/{category_id}")
    assert r.status_code == expected_status
    if expected_status == 200:
        assert r.json()["name"] == expected_name


@pytest.mark.parametrize(
    "category_id, update_data, expected_status",
    [
        (1, {"name": "Бытовая техника", "parent_id": None}, 200),
        (2, {"name": "iPhone", "parent_id": 1}, 200),
        (999, {"name": "Ghost", "parent_id": None}, 404),  # Ошибка: категории нет
        (1, {"name": "A", "parent_id": None}, 422),  # Ошибка: слишком короткое имя
    ],
    ids=[
        "success",
        "success",
        "category not found",
        "name_too_short"
    ]
)
@pytest.mark.asyncio
async def test_update_category(client, setup_database, category_id, update_data, expected_status):
    r = await client.put(f"/categories/{category_id}", json=update_data)
    assert r.status_code == expected_status
    if expected_status == 200:
        assert r.json()["name"] == update_data["name"]


@pytest.mark.parametrize(
    "category_id, expected_status",
    [
        (1, 204),
        (999, 404),
    ],
    ids=[
        "success",
        "category not found"
    ]
)
@pytest.mark.asyncio
async def test_delete_category(client, setup_database, category_id, expected_status):
    # Удаление
    r = await client.delete(f"/categories/{category_id}")
    assert r.status_code == expected_status

    # Проверка, что после 204 ресурс действительно пропал
    if expected_status == 204:
        check = await client.get(f"/categories/{category_id}")
        assert check.status_code == 404
