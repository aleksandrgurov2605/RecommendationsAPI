class CategoryNotFoundError(Exception):
    """Выбрасывается, когда категория не найдена."""

    def __init__(self, message: str = "Category not found"):
        self.message = message
        super().__init__(self.message)


class CategoryParentNotFoundError(Exception):
    """Выбрасывается, когда родительская категория не найдена."""

    def __init__(self, message: str = "Parent category not found"):
        self.message = message
        super().__init__(self.message)


class CategoryParentError(Exception):
    """Выбрасывается, когда категория указывает на саму себя в качестве родительской."""

    def __init__(self, message: str = "Category can't be its own parent"):
        self.message = message
        super().__init__(self.message)
