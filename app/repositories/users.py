from sqlalchemy import select

from app.models.users import User
from app.repositories.base_repository import Repository


class UserRepository(Repository[User]):
    model = User

    async def get_user(self, email: str) -> User | None:
        """
        Получить по условию where одну запись или None
        :param email:
        :return:
        """
        stmt = (
            select(self.model)
            .where(self.model.email == email)
            .where(self.model.is_active == True)  # noqa: E712
        )

        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
