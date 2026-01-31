from typing import Any

from sqlalchemy import select

from app.models.recommendations import Recommendation
from app.repositories.base_repository import Repository


class RecommendationRepository(Repository[Recommendation]):
    model = Recommendation

    async def fetch_one(self, **filter_by: Any) -> Recommendation | None:
        """
        Получить рекомендацию по фильтрам (например, user_id).
        :param filter_by:
        :return:
        """
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
