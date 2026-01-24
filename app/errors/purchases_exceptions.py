class PurchaseNotFoundError(Exception):
    """Выбрасывается, когда покупка не найдена."""

    def __init__(self, message: str = "Purchase not found"):
        self.message = message
        super().__init__(self.message)