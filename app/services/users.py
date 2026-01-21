from app.errors.users_exceptions import UserNotFoundError
from app.schemas.users import UserCreate, UserRead
from app.utils.unitofwork import IUnitOfWork


class UserService:
    @staticmethod
    async def add_user(uow: IUnitOfWork, user: UserCreate) -> UserRead:
        user_dict = user.model_dump()
        async with uow as uow:
            user_from_db = await uow.user.add_one(user_dict)
            user_to_return = UserRead.model_validate(user_from_db)
            await uow.commit()
            return user_to_return

    @staticmethod
    async def get_all_users(uow: IUnitOfWork) -> list[UserRead]:
        async with uow as uow:
            users_to_return = await uow.user.find_all()
            return [UserRead.model_validate(user) for user in users_to_return]

    @staticmethod
    async def get_user(uow: IUnitOfWork, user_id: int) -> UserRead:
        async with uow as uow:
            user_to_return = await uow.user.fetch_one(where=user_id)
            if not user_to_return:
                raise UserNotFoundError
            return UserRead.model_validate(user_to_return)

    @staticmethod
    async def update_user(uow: IUnitOfWork, user_id: int, user: UserCreate) -> UserRead:
        async with uow as uow:
            # Проверяем существование пользователя
            existing_user = await uow.user.fetch_one(where=user_id)
            if not existing_user:
                raise UserNotFoundError
            user_data = user.model_dump()
            user_to_return = await uow.user.update(data=user_data, where=user_id)
            if not user_to_return:
                raise UserNotFoundError
            await uow.commit()
            return UserRead.model_validate(user_to_return)

    @staticmethod
    async def delete_user(uow: IUnitOfWork, user_id: int):
        async with uow as uow:
            # Проверяем существование пользователя
            existing_user = await uow.user.fetch_one(where=user_id)
            if not existing_user:
                raise UserNotFoundError

            await uow.user.delete(where=user_id)
            await uow.commit()
