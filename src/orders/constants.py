from decimal import Decimal

from src.orders.models import PaymentMethod
from src.users.models import Segment

BASKET_SIZE_WEIGHTS = {1: 75, 2: 20, 3: 5}
QUANTITY_WEIGHTS = {1: 95, 2: 5}

PAYMENT_METHOD_WEIGHTS = {
    PaymentMethod.CARD: 60,
    PaymentMethod.CASH: 10,
    PaymentMethod.SBP: 28,
    PaymentMethod.CREDIT: 2,
}

SEGMENT_DISCOUNTS = {
    Segment.NEW: Decimal("0.000"),
    Segment.REGULAR: Decimal("0.050"),
    Segment.VIP: Decimal("0.100"),
}

CANCELLATION_PROBABILITY = 0.05
