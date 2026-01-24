from sqlalchemy import select, func

from app.models.purchases import Purchase, PurchaseUnit
from app.repositories.base_repository import Repository
from app.utils.logger import logger


class PurchaseRepository(Repository):
    model = Purchase

    async def get_purchases(self, **filter_by):
        """
        Получить покупки пользователя.
        :param filter_by:
        :return:
        """
        logger.debug(f"Starting PurchaseRepository.get_purchases")
        current_user_id = filter_by['current_user_id']
        page = filter_by['page']
        page_size = filter_by['page_size']

        stmt = (select(self.model)
                .where(self.model.user_id == current_user_id)
                .order_by(self.model.created_at.desc())
                .offset((page - 1) * page_size)
                .limit(page_size))

        purchases = await self.session.execute(stmt)
        return purchases.scalars().all()

    async def get_count_user_purchases(self, current_user_id: int):
        """
        Получить все записи из таблицы в БД, списком
        :return:
        """
        logger.debug(f"Starting PurchaseRepository.get_count_user_purchases")
        stmt = select(func.count(self.model.id)).where(self.model.user_id == current_user_id)
        count = await self.session.execute(stmt)
        return count.first()


class PurchaseUnitRepository(Repository):
    model = PurchaseUnit
