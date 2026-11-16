from clickhouse_connect.driver import Client

from src.users.models import Segment, User


class UserRepository:
    def __init__(self, client: Client) -> None:
        self._client = client

    def get_all(self) -> list[User]:
        result = self._client.query(
            "SELECT user_id, name, city, segment, registered_at "
            "FROM dim_users ORDER BY user_id"
        )
        return [
            User(user_id, name, city, Segment(segment), registered_at)
            for user_id, name, city, segment, registered_at in result.result_rows
        ]

    def add_many(self, users: list[User]) -> None:
        if not users:
            return

        rows = [
            (user.user_id, user.name, user.city, user.segment.value, user.registered_at)
            for user in users
        ]
        self._client.insert(
            "dim_users",
            rows,
            column_names=["user_id", "name", "city", "segment", "registered_at"],
        )
