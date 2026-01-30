from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.errors.users_exceptions import (
    CredentialsError,
    TokenHasExpiredError,
    UserNotFoundError,
)
from app.schemas.users import UserRead
from app.utils.logger import logger
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def create_access_token(data: dict):
    """
    Создаёт JWT с payload (sub, id, exp).
    :param data:
    :return:
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict):
    """
    Создаёт refresh-токен с длительным сроком действия.
    :param data:
    :return:
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_user(
    uow: Annotated[IUnitOfWork, Depends(UnitOfWork)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    """
    Проверяет JWT и возвращает пользователя из базы.
    :param uow:
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            logger.info("if email is None")
            raise CredentialsError
    except jwt.ExpiredSignatureError as err:
        logger.info("except jwt.ExpiredSignatureError")
        raise TokenHasExpiredError from err
    except jwt.PyJWTError as err:
        logger.info("except jwt.PyJWTError")
        raise CredentialsError from err
    async with uow as uow:
        user_to_return = await uow.user.get_user(email=email)
        if not user_to_return:
            logger.info("if not user_to_return")
            raise UserNotFoundError
        return UserRead.model_validate(user_to_return)
