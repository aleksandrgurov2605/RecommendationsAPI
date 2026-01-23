class UserNotFoundError(Exception):
    """Выбрасывается, когда пользователь не найден."""

    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(self.message)


class CredentialsError(Exception):
    """Выбрасывается, когда пользователь не предоставил актуальные данные."""

    def __init__(self, message: str = "Credentials exception"):
        self.message = message
        super().__init__(self.message)


class TokenHasExpiredError(Exception):
    """Выбрасывается, когда у токена истек срок действия."""

    def __init__(self, message: str = "Token has expired"):
        self.message = message
        super().__init__(self.message)

class EmailAlreadyTakenError(Exception):
    """Выбрасывается, когда пользователь предоставляет Email, который уже занят."""

    def __init__(self, message: str = "Email address is already in use"):
        self.message = message
        super().__init__(self.message)
