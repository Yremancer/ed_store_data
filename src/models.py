import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum


class Segment(StrEnum):
    NEW = "new"
    REGULAR = "regular"
    VIP = "vip"


class PaymentMethod(StrEnum):
    CARD = "card"
    CASH = "cash"
    SBP = "sbp"
    CREDIT = "credit"


class OrderStatus(StrEnum):
    PAID = "paid"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class User:
    user_id: int
    name: str
    city: str
    segment: Segment
    registered_at: datetime


@dataclass(frozen=True, slots=True)
class Product:
    product_id: int
    name: str
    category: str
    base_price: Decimal


@dataclass(frozen=True, slots=True)
class OrderItem:
    order_id: uuid.UUID
    order_ts: datetime
    user_id: int
    product_id: int
    quantity: int
    price: Decimal
    discount: Decimal
    payment_method: PaymentMethod
    status: OrderStatus
