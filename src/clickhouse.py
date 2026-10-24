import clickhouse_connect
from clickhouse_connect.driver import Client

from src.config import get_settings


def create_client() -> Client:
    settings = get_settings()
    return clickhouse_connect.get_client(
        host=settings.CLICKHOUSE_HOST,
        port=settings.CLICKHOUSE_PORT,
        username=settings.CLICKHOUSE_USER,
        password=settings.CLICKHOUSE_PASSWORD,
        database=settings.CLICKHOUSE_DB,
    )
