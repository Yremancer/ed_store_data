from datetime import datetime


class InvalidOrderCountError(ValueError):
    def __init__(self, count: int) -> None:
        self.count = count
        super().__init__(f"Order count must be positive, got {count}")


class EmptyOrderCatalogError(ValueError):
    def __init__(self, catalog: str) -> None:
        self.catalog = catalog
        super().__init__(f"Cannot generate orders: {catalog} catalog is empty")


class InvalidDemandError(ValueError):
    pass


class InvalidDemandTimestampError(InvalidDemandError):
    def __init__(self, timestamp: datetime) -> None:
        self.timestamp = timestamp
        super().__init__(
            f"Demand timestamp must include a timezone, got {timestamp!r}"
        )


class InvalidAnomalyWindowError(InvalidDemandError):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(f"Invalid anomaly window: {reason}")


class InvalidDemandFactorError(InvalidDemandError):
    def __init__(self, factor: str, value: float) -> None:
        self.factor = factor
        self.value = value
        super().__init__(f"Demand factor {factor!r} must be finite and non-negative")


class InvalidExpectedOrderCountError(InvalidDemandError):
    def __init__(self, expected: float) -> None:
        self.expected = expected
        super().__init__(
            f"Expected order count must be finite and non-negative, got {expected!r}"
        )
