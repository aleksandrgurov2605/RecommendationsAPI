from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.dependencies import UOWDep, UserDep
from app.schemas.users import UserCreate, UserRead
from app.services.users import UserService
from app.utils.logger import logger

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=list[UserRead])
async def get_all_users(uow: UOWDep):
    """
    Получить список всех активных пользователей.
    :param uow:
    :return:
    """
    logger.info("Получить список всех активных пользователей.")
    categories = await UserService.get_all_users(uow)
    return categories


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(uow: UOWDep, user: UserCreate):
    """
    Создать нового пользователя.
    :param uow:
    :param user:
    :return:
    """
    logger.info(f"Создать нового пользователя с {user.email=}.")
    user_created = await UserService.add_user(uow, user)
    return user_created


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(uow: UOWDep, user_id: int):
    """
    Получить активного пользователя по id.
    :param uow:
    :param user_id:
    :return:
    """
    logger.info(f"Получить активного пользователя по id = {user_id}.")
    user = await UserService.get_user(uow, user_id)
    return user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    uow: UOWDep, current_user: UserDep, user_id: int, user: UserCreate
):
    """
    Обновить пользователя по id.
    :param uow:
    :param user_id:
    :param user:
    :return:
    """
    logger.info(f"Обновить пользователя по id = {user_id}.")
    user_updated = await UserService.update_user(uow, user_id, user)
    return user_updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(uow: UOWDep, current_user: UserDep, user_id: int):
    """
    Удалить пользователя по id.
    :param uow:
    :param user_id:
    :return:
    """
    logger.info(f"Удалить пользователя по id = {user_id}.")
    await UserService.delete_user(uow, user_id)
    return {"message": f"User {user_id} was deleted."}


@router.post("/token")
async def login(
    uow: UOWDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> dict[str, str]:
    """
    Аутентифицировать пользователя и получить access_token и refresh_token.
    :param uow:
    :param form_data:
    :return:
    """
    logger.info(
        "Аутентифицировать пользователя и получить access_token и refresh_token."
    )
    result = await UserService.login(uow, form_data)
    return result


@router.post("/refresh-token")
async def refresh_token(
    uow: UOWDep, current_user: UserDep, user_refresh_token: str = Body(embed=True)
):
    """
    Обновляет access_token с помощью refresh_token.
    :param uow:
    :param user_refresh_token:
    :return:
    """
    logger.info(f"{current_user=}")
    access_token = await UserService.refresh_token(uow, user_refresh_token)
    return {"access_token": access_token, "token_type": "bearer"}
