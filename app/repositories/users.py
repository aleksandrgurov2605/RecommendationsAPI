from pydantic import BaseModel
from sqlalchemy import select, insert, update

from app.models.users import User
from app.repositories.base_repository import Repository
from app.utils.logger import logger
from app.utils.security import get_password_hash


class UserRepository(Repository):
    model = User

    async def get_user(self, email: str) -> BaseModel | None:
        """
        Получить по условию where одну запись или None
        :param email:
        :return:
        """
        logger.info(f"Starting UserRepository.get_user")
        stmt = select(self.model).where(self.model.email == email).where(self.model.is_active == True)

        res  = await self.session.execute(stmt)
        return res.scalar_one_or_none()
