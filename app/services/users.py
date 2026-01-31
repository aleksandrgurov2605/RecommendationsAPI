import jwt
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.errors.users_exceptions import (
    CredentialsError,
    EmailAlreadyTakenError,
    TokenHasExpiredError,
    UserNotFoundError,
)
from app.schemas.users import UserCreate, UserRead
from app.utils.auth import create_access_token, create_refresh_token
from app.utils.security import get_password_hash, verify_password
from app.utils.unitofwork import IUnitOfWork


class UserService:
    @staticmethod
    async def get_all_users(uow: IUnitOfWork) -> list[UserRead]:
        """
        Получить список всех активных пользователей.
        :param uow:
        :return:
        """
        async with uow:
            users_to_return = await uow.user.find_all()
            return [UserRead.model_validate(user) for user in users_to_return]

    @staticmethod
    async def add_user(uow: IUnitOfWork, user: UserCreate) -> UserRead:
        """
        Создать нового пользователя.
        :param uow:
        :param user:
        :return:
        """
        user_data = user.model_dump()
        user_data["password"] = get_password_hash(user_data["password"])

        async with uow:
            try:
                user_from_db = await uow.user.add_one(user_data)
            except IntegrityError as err:
                raise EmailAlreadyTakenError from err
            user_to_return = UserRead.model_validate(user_from_db)
            await uow.commit()
            return user_to_return

    @staticmethod
    async def get_user(uow: IUnitOfWork, user_id: int) -> UserRead:
        """
        Получить активного пользователя по id.
        :param uow:
        :param user_id:
        :return:
        """
        async with uow as uow:
            user_to_return = await uow.user.fetch_one(id=user_id)
            if not user_to_return:
                raise UserNotFoundError
            return UserRead.model_validate(user_to_return)

    @staticmethod
    async def update_user(uow: IUnitOfWork, user_id: int, user: UserCreate) -> UserRead:
        """
        Обновить пользователя по id.
        :param uow:
        :param user_id:
        :param user:
        :return:
        """
        user_data = user.model_dump()
        user_data["password"] = get_password_hash(user_data["password"])
        async with uow as uow:
            # Проверяем существование пользователя
            existing_user = await uow.user.fetch_one(id=user_id)
            if not existing_user:
                raise UserNotFoundError
            try:
                user_updated  = await uow.user.update(data=user_data, id=user_id)
                if not user_updated:
                    raise UserNotFoundError
                await uow.commit()
                return UserRead.model_validate(user_updated)
            except IntegrityError as err:
                raise EmailAlreadyTakenError from err


    @staticmethod
    async def delete_user(uow: IUnitOfWork, user_id: int) -> None:
        """
        Удалить пользователя по id.
        :param uow:
        :param user_id:
        :return:
        """
        async with uow as uow:
            # Проверяем существование пользователя
            existing_user = await uow.user.fetch_one(id=user_id)
            if not existing_user:
                raise UserNotFoundError

            await uow.user.delete(id=user_id)
            await uow.commit()

    @staticmethod
    async def login(
            uow: IUnitOfWork, form_data: OAuth2PasswordRequestForm
    ) -> dict[str, str]:
        """
        Аутентифицировать пользователя и получить access_token и refresh_token.
        :param uow:
        :param form_data:
        :return:
        """
        async with uow as uow:
            # Проверяем существование пользователя
            user = await uow.user.get_user(email=form_data.username)
            if not user or not verify_password(form_data.password, user.password):
                raise CredentialsError

            access_token = create_access_token(data={"sub": user.email, "id": user.id})
            refresh_token = create_refresh_token(
                data={"sub": user.email, "id": user.id}
            )
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }

    @staticmethod
    async def refresh_token(uow: IUnitOfWork, refresh_token: str) -> dict[str, str]:
        """
        Обновляет access_token с помощью refresh_token.
        :param uow:
        :param refresh_token:
        :return:
        """
        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            email: str = payload.get("sub")
            if email is None:
                raise CredentialsError
        except jwt.ExpiredSignatureError as err:
            # refresh-токен истёк
            raise TokenHasExpiredError from err
        except jwt.PyJWTError as err:
            # подпись неверна или токен повреждён
            raise CredentialsError from err
        async with uow as uow:
            # Проверяем существование пользователя
            user = await uow.user.get_user(email=email)
            if user is None:
                raise CredentialsError
            access_token = create_access_token(data={"sub": user.email, "id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}
