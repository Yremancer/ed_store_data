class InvalidUserCountError(ValueError):
    def __init__(self, count: int, max_count: int) -> None:
        self.count = count
        self.max_count = max_count
        super().__init__(
            f"User count must be between 1 and {max_count}, got {count}"
        )
