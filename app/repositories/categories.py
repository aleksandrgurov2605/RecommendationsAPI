from app.models.categories import Category
from app.repositories.base_repository import Repository
from app.utils.logger import logger


class CategoryRepository(Repository):
    model = Category

    logger.debug(f"Starting CategoryRepository")