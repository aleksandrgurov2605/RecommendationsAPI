from pydantic import BaseModel
from sqlalchemy import select

from app.models.recommendations import Recommendation
from app.repositories.base_repository import Repository


class RecommendationRepository(Repository):
    model = Recommendation

    async def fetch_one(self, user_id: int) -> BaseModel | None:
        """
        Получить одну запись по user_id или None
        :param user_id:
        :return:
        """
        stmt = select(self.model).where(self.model.user_id == user_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
