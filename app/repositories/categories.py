from app.models.categories import Category
from app.repositories.base_repository import Repository


class CategoryRepository(Repository):
    model = Category
