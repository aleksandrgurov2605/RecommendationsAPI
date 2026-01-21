from app.errors.categories_exceptions import CategoryNotFoundError
from app.errors.items_exceptions import ItemNotFoundError, WrongCategoryNotFoundError
from app.schemas.items import ItemCreate, ItemRead
from app.utils.unitofwork import IUnitOfWork


class ItemService:
    @staticmethod
    async def add_item(uow: IUnitOfWork, item: ItemCreate) -> ItemRead:
        async with uow as uow:
            # Проверяем существование категории
            existing_category = await uow.category.fetch_one(where=item.category_id)
            if not existing_category:
                raise WrongCategoryNotFoundError
            item_dict = item.model_dump()
            item_from_db = await uow.item.add_one(item_dict)
            item_to_return = ItemRead.model_validate(item_from_db)
            await uow.commit()
            return item_to_return

    @staticmethod
    async def get_all_items(uow: IUnitOfWork) -> list[ItemRead]:
        async with uow as uow:
            items_to_return = await uow.item.find_all()
            return [ItemRead.model_validate(item) for item in items_to_return]

    @staticmethod
    async def get_item(uow: IUnitOfWork, item_id: int) -> ItemRead:
        async with uow as uow:
            item_to_return = await uow.item.fetch_one(where=item_id)
            if not item_to_return:
                raise ItemNotFoundError
            return ItemRead.model_validate(item_to_return)

    @staticmethod
    async def update_item(uow: IUnitOfWork, item_id: int, item: ItemCreate) -> ItemRead:
        async with uow as uow:
            # Проверяем существование товара
            existing_item = await uow.item.fetch_one(where=item_id)
            if not existing_item:
                raise ItemNotFoundError

            # Проверяем существование категории
            existing_category = await uow.category.fetch_one(where=item.category_id)
            if not existing_category:
                raise WrongCategoryNotFoundError

            item_data = item.model_dump()
            item_to_return = await uow.item.update(data=item_data, where=item_id)
            if not item_to_return:
                raise ItemNotFoundError
            await uow.commit()
            return ItemRead.model_validate(item_to_return)

    @staticmethod
    async def delete_item(uow: IUnitOfWork, item_id: int):
        async with uow as uow:
            # Проверяем существование товара
            existing_item = await uow.item.fetch_one(where=item_id)
            if not existing_item:
                raise ItemNotFoundError

            await uow.item.delete(where=item_id)
            await uow.commit()
