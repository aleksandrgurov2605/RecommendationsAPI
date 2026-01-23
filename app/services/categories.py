from app.errors.categories_exceptions import CategoryParentNotFoundError, CategoryNotFoundError, CategoryParentError
from app.schemas.categories import CategoryCreate, CategoryRead
from app.utils.unitofwork import IUnitOfWork


class CategoryService:
    @staticmethod
    async def add_category(
            uow: IUnitOfWork,
            category: CategoryCreate
    ) -> CategoryRead:
        """

        :param uow:
        :param category:
        :return:
        """
        if category.parent_id is not None:
            async with uow as uow:
                parent = await uow.category.fetch_one(where=category.parent_id)
                if parent is None:
                    raise CategoryParentNotFoundError
        category_dict = category.model_dump()
        async with uow as uow:
            category_from_db = await uow.category.add_one(category_dict)
            category_to_return = CategoryRead.model_validate(category_from_db)
            await uow.commit()
            return category_to_return

    @staticmethod
    async def get_all_categories(
            uow: IUnitOfWork
    ) -> list[CategoryRead]:
        """
        Получить список всех активных категорий.
        :param uow:
        :return:
        """
        async with uow as uow:
            categories_to_return = await uow.category.find_all()
            return [CategoryRead.model_validate(category) for category in categories_to_return]

    @staticmethod
    async def get_category(
            uow: IUnitOfWork,
            category_id: int
    ) -> CategoryRead:
        """
        Получить активную категорию по id.
        :param uow:
        :param category_id:
        :return:
        """
        async with uow as uow:
            category_to_return = await uow.category.fetch_one(where=category_id)
            if not category_to_return:
                raise CategoryNotFoundError
            return CategoryRead.model_validate(category_to_return)

    @staticmethod
    async def update_category(
            uow: IUnitOfWork,
            category_id: int,
            category: CategoryCreate
    ) -> CategoryRead:
        """
        Обновить категорию по id.
        :param uow:
        :param category_id:
        :param category:
        :return:
        """
        async with uow as uow:
            # Проверяем существование категории
            existing_category = await uow.category.fetch_one(where=category_id)
            if not existing_category:
                raise CategoryNotFoundError
            # Проверяем существование родительской категории
            if category.parent_id is not None:
                parent = await uow.category.fetch_one(where=category.parent_id)
                if parent is None:
                    raise CategoryParentNotFoundError
                if parent.id == category_id:
                    raise CategoryParentError
            category_data = category.model_dump()
            category_to_return = await uow.category.update(data=category_data, where=category_id)
            if not category_to_return:
                raise CategoryNotFoundError
            await uow.commit()
            return CategoryRead.model_validate(category_to_return)

    @staticmethod
    async def delete_category(
            uow: IUnitOfWork,
            category_id: int
    ) -> None:
        """
        Удалить категорию по id.
        :param uow:
        :param category_id:
        :return:
        """
        async with uow as uow:
            # Проверяем существование категории
            existing_category = await uow.category.fetch_one(where=category_id)
            if not existing_category:
                raise CategoryNotFoundError

            await uow.category.delete(where=category_id)
            await uow.commit()
