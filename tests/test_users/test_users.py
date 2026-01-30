import pytest


@pytest.mark.parametrize(
    "data, expected_status",
    [
        ({"email": "fake1@mail.com", "name": "name", "password": "password"}, 201),
        ({"email": "fake2@mail.com", "name": "name", "password": "password"}, 201),
        ({"email": "incorrect_email", "name": "name", "password": "password"}, 422),
        ({"email": "fake5@mail.com", "name": "", "password": "password"}, 422),
        ({"email": "fake_email6@mail.com", "name": "e", "password": "password"}, 422),
        (
            {"email": "prepair@mail.com", "name": "Duplicate", "password": "password"},
            409,
        ),
    ],
    ids=[
        "success",
        "success",
        "incorrect_email",
        "empty_name",
        "name_too_short",
        "already_exist",
    ],
)
@pytest.mark.asyncio
async def test_create_user(client, setup_database, data, expected_status):
    r = await client.post(
        "/users/",
        json=data,
    )
    assert r.status_code == expected_status


@pytest.mark.asyncio
async def test_get_all_users(client, setup_database):
    users_from_db = await client.get("/users/")
    assert users_from_db.status_code == 200
    assert len(users_from_db.json()) == 2
    assert users_from_db.json()[0]["name"] == "User"
    assert users_from_db.json()[1]["name"] == "TwoUser"


@pytest.mark.parametrize(
    "user_id, expected_status, expected_name",
    [
        (1, 200, "User"),
        (999, 404, None),
    ],
    ids=["success", "wrong ID"],
)
@pytest.mark.asyncio
async def test_get_user_by_id(
    client, setup_database, user_id, expected_status, expected_name
):
    r = await client.get(f"/users/{user_id}")
    assert r.status_code == expected_status
    if expected_status == 200:
        assert r.json()["name"] == expected_name


@pytest.mark.parametrize(
    "user_id, update_data, expected_status",
    [
        (1, {"email": "fake1@mail.com", "name": "name", "password": "password"}, 200),
        (2, {"email": "fake2@mail.com", "name": "name", "password": "password"}, 200),
        (999, {"email": "fake1@mail.com", "name": "name", "password": "password"}, 404),
        (1, {"email": "fake1@mail.com", "name": "", "password": "password"}, 422),
    ],
    ids=["success", "success", "user not found", "name_too_short"],
)
@pytest.mark.asyncio
async def test_update_user(
    client, setup_database, auth_headers, user_id, update_data, expected_status
):
    r = await client.put(f"/users/{user_id}", json=update_data, headers=auth_headers)
    assert r.status_code == expected_status
    if expected_status == 200:
        assert r.json()["name"] == update_data["name"]


@pytest.mark.parametrize(
    "user_id, expected_status",
    [
        (1, 204),
        (999, 404),
    ],
    ids=["success", "user not found"],
)
@pytest.mark.asyncio
async def test_delete_user(
    client, setup_database, auth_headers, user_id, expected_status
):
    # Удаление
    r = await client.delete(f"/users/{user_id}", headers=auth_headers)
    assert r.status_code == expected_status

    # Проверка, что после 204 ресурс действительно пропал
    if expected_status == 204:
        check = await client.get(f"/users/{user_id}")
        assert check.status_code == 404
