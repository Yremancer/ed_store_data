from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class SupersetSettings(BaseSettings):
    model_config = SettingsConfigDict(hide_input_in_errors=True)

    SUPERSET_SECRET_KEY: SecretStr = Field(min_length=1)
    SUPERSET_ADMIN_USER: str = Field(default="admin", min_length=1)
    SUPERSET_ADMIN_FIRST_NAME: str = Field(default="Superset", min_length=1)
    SUPERSET_ADMIN_LAST_NAME: str = Field(default="Admin", min_length=1)
    SUPERSET_ADMIN_EMAIL: str = Field(default="admin@example.com", min_length=1)
    SUPERSET_ADMIN_PASSWORD: SecretStr = Field(min_length=1)
    POSTGRES_PASSWORD: SecretStr = Field(min_length=1)
    POSTGRES_USER: str = "postgres"
    POSTGRES_DB: str | None = None
    CLICKHOUSE_HOST: str = Field(min_length=1)
    CLICKHOUSE_PORT: int = Field(ge=1, le=65535)
    CLICKHOUSE_DB: str = Field(min_length=1)
    CLICKHOUSE_USER: str = Field(min_length=1)
    CLICKHOUSE_PASSWORD: SecretStr

    @property
    def postgres_url(self) -> URL:
        return URL.create(
            "postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host="superset-postgres",
            port=5432,
            database=self.POSTGRES_DB or self.POSTGRES_USER,
        )

    @property
    def clickhouse_url(self) -> URL:
        return URL.create(
            "clickhousedb",
            username=self.CLICKHOUSE_USER,
            password=self.CLICKHOUSE_PASSWORD.get_secret_value(),
            host=self.CLICKHOUSE_HOST,
            port=self.CLICKHOUSE_PORT,
            database=self.CLICKHOUSE_DB,
        )


settings = SupersetSettings()

SECRET_KEY = settings.SUPERSET_SECRET_KEY.get_secret_value()
SQLALCHEMY_DATABASE_URI = settings.postgres_url.render_as_string(hide_password=False)

DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_URL": "redis://superset-redis:6379/0",
    "CACHE_KEY_PREFIX": "ed_store_charts:",
    "CACHE_DEFAULT_TIMEOUT": 15,
}
