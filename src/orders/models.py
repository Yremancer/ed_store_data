from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID


class PaymentMethod(StrEnum):
    CARD = "card"
    CASH = "cash"
    SBP = "sbp"
    CREDIT = "credit"


class OrderStatus(StrEnum):
    PAID = "paid"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class OrderItem:
    order_id: UUID
    order_ts: datetime
    user_id: int
    product_id: int
    quantity: int
    price: Decimal
    discount: Decimal
    payment_method: PaymentMethod
    status: OrderStatus
