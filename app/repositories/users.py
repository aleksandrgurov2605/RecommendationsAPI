from app.models.users import User
from app.repositories.base_repository import Repository

class UserRepository(Repository):
    model = User