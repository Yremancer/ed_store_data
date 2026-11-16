from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.users.constants import CITIES, NAMES


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASSWORD: str
    CLICKHOUSE_DB: str
    LOG_LEVEL: str = "INFO"
    GENERATOR_USERS_COUNT: int = Field(default=300, ge=1, le=len(NAMES) * len(CITIES))
    GENERATOR_SEED: int = 42
    GENERATOR_ORDERS_PER_BATCH: int = Field(default=5, ge=1)
    GENERATOR_INTERVAL_SECONDS: float = Field(default=2.0, gt=0, allow_inf_nan=False)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
