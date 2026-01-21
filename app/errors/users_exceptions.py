class UserNotFoundError(Exception):
    """Выбрасывается, когда пользователь не найден."""

    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(self.message)



