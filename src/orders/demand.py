from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from math import cos, floor, isfinite, pi
from random import Random

from src.orders.constants import LOCAL_TIMEZONE
from src.orders.exceptions import (
    InvalidAnomalyWindowError,
    InvalidDemandFactorError,
    InvalidDemandTimestampError,
    InvalidExpectedOrderCountError,
    InvalidOrderCountError,
)

@dataclass(frozen=True, slots=True)
class HolidayDemandProfile:
    month: int
    day: int
    days_before_peak: int
    days_after_peak: int
    peak_multiplier: float


HOLIDAY_PROFILES = (
    HolidayDemandProfile(12, 31, 21, 2, 2.2),
    HolidayDemandProfile(2, 14, 10, 1, 1.7),
    HolidayDemandProfile(3, 8, 14, 1, 2.0),
)


@dataclass(frozen=True, slots=True)
class DemandFactors:
    daily: float
    holiday: float
    trend: float
    anomaly: float

    @property
    def total(self) -> float:
        return self.daily * self.holiday * self.trend * self.anomaly


def _local_time(at: datetime) -> datetime:
    if at.utcoffset() is None:
        raise InvalidDemandTimestampError(at)
    return at.astimezone(LOCAL_TIMEZONE)


def _smooth_growth(progress: float, peak_multiplier: float) -> float:
    return 1 + (peak_multiplier - 1) * (1 - cos(pi * progress)) / 2


def daily_factor(at: datetime) -> float:
    local_at = _local_time(at)
    hour = local_at.hour + local_at.minute / 60 + local_at.second / 3600
    return 1 + 0.65 * cos(2 * pi * (hour - 18) / 24)


def _holiday_peak(profile: HolidayDemandProfile, year: int) -> datetime:
    peak_date = date(year, profile.month, profile.day)
    return datetime.combine(peak_date, time(18), tzinfo=LOCAL_TIMEZONE)


def _holiday_window_factor(
    at: datetime,
    profile: HolidayDemandProfile,
    year: int,
) -> float:
    peak = _holiday_peak(profile, year)
    window_start = peak - timedelta(days=profile.days_before_peak)
    window_end = peak + timedelta(days=profile.days_after_peak)

    if not window_start <= at < window_end:
        return 1.0

    if at <= peak:
        progress = (at - window_start) / (peak - window_start)
    else:
        progress = (window_end - at) / (window_end - peak)

    return _smooth_growth(progress, profile.peak_multiplier)


def holiday_factor(at: datetime) -> float:
    local_at = _local_time(at)
    candidate_years = range(local_at.year - 1, local_at.year + 2)
    return max(
        _holiday_window_factor(local_at, profile, year)
        for profile in HOLIDAY_PROFILES
        for year in candidate_years
    )


def trend_factor(at: datetime, start_date: date) -> float:
    local_date = _local_time(at).date()
    elapsed_days = max(0, (local_date - start_date).days)
    return min(1.30, 1 + 0.005 * elapsed_days)


def _utc_time(at: datetime) -> datetime:
    if at.utcoffset() is None:
        raise InvalidDemandTimestampError(at)
    return at.astimezone(UTC)


def anomaly_factor(
    at: datetime,
    start: datetime | None,
    duration_minutes: int,
    multiplier: float,
) -> float:
    if start is None:
        return 1.0
    if duration_minutes <= 0:
        raise InvalidAnomalyWindowError("duration must be greater than zero")
    if not isfinite(multiplier) or multiplier <= 0:
        raise InvalidAnomalyWindowError(
            "multiplier must be finite and greater than zero"
        )

    current_time = _utc_time(at)
    window_start = _utc_time(start)
    window_end = window_start + timedelta(minutes=duration_minutes)
    return multiplier if window_start <= current_time < window_end else 1.0


def demand_factors(
    at: datetime,
    trend_start_date: date,
    anomaly_start: datetime | None,
    anomaly_duration_minutes: int,
    anomaly_multiplier: float,
) -> DemandFactors:
    return DemandFactors(
        daily=daily_factor(at),
        holiday=holiday_factor(at),
        trend=trend_factor(at, trend_start_date),
        anomaly=anomaly_factor(
            at,
            anomaly_start,
            anomaly_duration_minutes,
            anomaly_multiplier,
        ),
    )


def expected_orders(base_orders_per_batch: int, factors: DemandFactors) -> float:
    if base_orders_per_batch < 1:
        raise InvalidOrderCountError(base_orders_per_batch)

    expected = base_orders_per_batch * factors.total
    if not isfinite(expected) or expected < 0:
        raise InvalidExpectedOrderCountError(expected)
    return expected


def sample_order_count(expected: float, rng: Random) -> int:
    if not isfinite(expected) or expected < 0:
        raise InvalidExpectedOrderCountError(expected)

    whole_orders = floor(expected)
    fractional_orders = expected - whole_orders
    return whole_orders + int(
        fractional_orders > 0 and rng.random() < fractional_orders
    )
