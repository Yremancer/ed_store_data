class InvalidOrderCountError(ValueError):
    def __init__(self, count: int) -> None:
        self.count = count
        super().__init__(f"Order count must be positive, got {count}")


class EmptyOrderCatalogError(ValueError):
    def __init__(self, catalog: str) -> None:
        self.catalog = catalog
        super().__init__(f"Cannot generate orders: {catalog} catalog is empty")
