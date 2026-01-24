class CartUnitNotFoundError(Exception):
    """Выбрасывается, когда CartUnit не найден."""

    def __init__(self, message: str = "CartUnit not found"):
        self.message = message
        super().__init__(self.message)


class NotEnoughItemsError(Exception):
    """Выбрасывается, когда в корзине больше единиц товара, чем осталось на складе."""

    def __init__(self, message: str = "Not enough items in stock"):
        self.message = message
        super().__init__(self.message)
