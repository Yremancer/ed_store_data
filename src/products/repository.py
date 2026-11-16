from clickhouse_connect.driver import Client

from src.products.models import Product


class ProductRepository:
    def __init__(self, client: Client) -> None:
        self._client = client

    def get_all(self) -> list[Product]:
        result = self._client.query(
            "SELECT product_id, name, category, material_category, base_price "
            "FROM dim_products ORDER BY product_id"
        )
        return [Product(*row) for row in result.result_rows]
