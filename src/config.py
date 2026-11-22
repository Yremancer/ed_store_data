from datetime import date, datetime
from functools import lru_cache

from pydantic import Field, field_validator
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
    GENERATOR_SEED: int = Field(
        default=42,
        description="Seed for reproducible order generation and count rounding",
    )
    GENERATOR_ORDERS_PER_BATCH: int = Field(
        default=5,
        ge=1,
        description="Baseline expected orders per pass when demand factors equal 1.0",
    )
    GENERATOR_INTERVAL_SECONDS: float = Field(
        default=2.0,
        gt=0,
        allow_inf_nan=False,
        description="Wait time between generation passes",
    )
    GENERATOR_TREND_START_DATE: date = Field(
        default=date(2026, 11, 22),
        description="Local date when demand trend starts",
    )
    GENERATOR_ANOMALY_START: datetime | None = Field(
        default=None,
        description="Timezone-aware start of the demand anomaly window",
    )
    GENERATOR_ANOMALY_DURATION_MINUTES: int = Field(
        default=10,
        gt=0,
        description="Duration of the anomaly window in minutes",
    )
    GENERATOR_ANOMALY_MULTIPLIER: float = Field(
        default=4.0,
        gt=0,
        allow_inf_nan=False,
        description="Demand multiplier during the anomaly window",
    )

    @field_validator("GENERATOR_ANOMALY_START")
    @classmethod
    def anomaly_start_must_include_timezone(
        cls, value: datetime | None
    ) -> datetime | None:
        if value is not None and value.utcoffset() is None:
            raise ValueError("GENERATOR_ANOMALY_START must include a timezone offset")
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
