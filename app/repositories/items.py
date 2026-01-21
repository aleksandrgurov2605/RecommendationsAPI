from app.models.items import Item
from app.repositories.base_repository import Repository

class ItemRepository(Repository):
    model = Item