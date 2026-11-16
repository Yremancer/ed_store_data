from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from random import Random
from uuid import uuid4

from src.orders.constants import (
    BASKET_SIZE_WEIGHTS,
    CANCELLATION_PROBABILITY,
    PAYMENT_METHOD_WEIGHTS,
    QUANTITY_WEIGHTS,
    SEGMENT_DISCOUNTS,
)
from src.orders.exceptions import EmptyOrderCatalogError, InvalidOrderCountError
from src.orders.models import OrderItem, OrderStatus
from src.products.models import Product
from src.users.models import User


def generate_orders(
    count: int,
    users: list[User],
    products: list[Product],
    rng: Random,
    now: datetime,
) -> list[OrderItem]:
    if count < 1:
        raise InvalidOrderCountError(count)
    if not users:
        raise EmptyOrderCatalogError("users")
    if not products:
        raise EmptyOrderCatalogError("products")

    items = []

    for _ in range(count):
        order_id = uuid4()
        user = rng.choice(users)
        basket_size = rng.choices(
            tuple(BASKET_SIZE_WEIGHTS),
            weights=tuple(BASKET_SIZE_WEIGHTS.values()),
            k=1,
        )[0]
        basket = rng.sample(products, min(basket_size, len(products)))
        discount = SEGMENT_DISCOUNTS[user.segment]
        payment_method = rng.choices(
            tuple(PAYMENT_METHOD_WEIGHTS),
            weights=tuple(PAYMENT_METHOD_WEIGHTS.values()),
            k=1,
        )[0]
        status = (
            OrderStatus.CANCELLED
            if rng.random() < CANCELLATION_PROBABILITY
            else OrderStatus.PAID
        )

        for product in basket:
            quantity = rng.choices(
                tuple(QUANTITY_WEIGHTS),
                weights=tuple(QUANTITY_WEIGHTS.values()),
                k=1,
            )[0]
            price = (product.base_price * (Decimal(1) - discount)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            items.append(
                OrderItem(
                    order_id=order_id,
                    order_ts=now,
                    user_id=user.user_id,
                    product_id=product.product_id,
                    quantity=quantity,
                    price=price,
                    discount=discount,
                    payment_method=payment_method,
                    status=status,
                )
            )

    return items
