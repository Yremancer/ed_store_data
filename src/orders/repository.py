from typing import Protocol

from clickhouse_connect.driver import Client

from src.orders.models import OrderItem


class OrderWriter(Protocol):
    def add_many(self, items: list[OrderItem]) -> None: ...


class OrderRepository:
    def __init__(self, client: Client) -> None:
        self._client = client

    def add_many(self, items: list[OrderItem]) -> None:
        if not items:
            return

        rows = [
            (
                item.order_id,
                item.order_ts,
                item.user_id,
                item.product_id,
                item.quantity,
                item.price,
                item.discount,
                item.payment_method.value,
                item.status.value,
            )
            for item in items
        ]
        self._client.insert(
            "fact_order_items",
            rows,
            column_names=[
                "order_id",
                "order_ts",
                "user_id",
                "product_id",
                "quantity",
                "price",
                "discount",
                "payment_method",
                "status",
            ],
        )
