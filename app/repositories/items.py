from sqlalchemy import select

from app.models.items import Item
from app.repositories.base_repository import Repository
from app.utils.logger import logger


class ItemRepository(Repository):
    model = Item

    async def get_active_item(self, item_id: int):
        """
        Получить активный товар из БД.
        :param item_id:
        :return:
        """
        logger.debug(f"Starting ItemRepository.get_active_item")
        stmt = select(self.model).where(
            self.model.id == item_id,
            self.model.is_active == True,
        )
        item = await self.session.execute(stmt)
        return item.scalar_one_or_none()
