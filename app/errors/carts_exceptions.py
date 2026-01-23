class CartUnitNotFoundError(Exception):
    """Выбрасывается, когда CartUnit не найден."""

    def __init__(self, message: str = "CartUnit not found"):
        self.message = message
        super().__init__(self.message)
