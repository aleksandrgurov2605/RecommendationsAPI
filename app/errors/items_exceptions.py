class ItemNotFoundError(Exception):
    """Выбрасывается, когда товар не найден."""

    def __init__(self, message: str = "Item not found"):
        self.message = message
        super().__init__(self.message)


class WrongCategoryNotFoundError(Exception):
    """Выбрасывается, когда при создании товара указана категория, отсутствующая в БД."""

    def __init__(self, message: str = "Wrong category_id", code: int = 422):
        self.message = message
        self.code = code
        super().__init__(self.message, self.code)


class ItemHasNoPriceError(Exception):
    """Выбрасывается, когда у товара не указана цена."""

    def __init__(self, message: str = "Item has no price"):
        self.message = message
        super().__init__(self.message)
