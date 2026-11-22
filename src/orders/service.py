import logging
import threading
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from random import Random

from src.clock import utc_now
from src.config import Settings
from src.orders.demand import demand_factors, expected_orders, sample_order_count
from src.orders.exceptions import InvalidDemandTimestampError
from src.orders.generator import generate_orders
from src.orders.models import OrderItem
from src.orders.repository import OrderWriter
from src.products.models import Product
from src.users.models import User

Clock = Callable[[], datetime]

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class OrderBatchResult:
    expected_orders: float
    order_count: int
    item_count: int


class OrderGenerationService:
    def __init__(
        self,
        *,
        settings: Settings,
        users: list[User],
        products: list[Product],
        repository: OrderWriter,
        stop_event: threading.Event,
        clock: Clock = utc_now,
    ) -> None:
        self._settings = settings
        self._users = users
        self._products = products
        self._repository = repository
        self._stop_event = stop_event
        self._clock = clock
        self._order_rng = Random(settings.GENERATOR_SEED)
        self._count_rng = Random(settings.GENERATOR_SEED)

    def run(self) -> None:
        self._log_anomaly_window()
        while not self._stop_event.is_set():
            self.run_once()
            self._stop_event.wait(self._settings.GENERATOR_INTERVAL_SECONDS)

    def run_once(self) -> OrderBatchResult:
        now = self._clock()
        if now.utcoffset() is None:
            raise InvalidDemandTimestampError(now)
        now = now.astimezone(UTC).replace(microsecond=0)

        factors = demand_factors(
            at=now,
            trend_start_date=self._settings.GENERATOR_TREND_START_DATE,
            anomaly_start=self._settings.GENERATOR_ANOMALY_START,
            anomaly_duration_minutes=self._settings.GENERATOR_ANOMALY_DURATION_MINUTES,
            anomaly_multiplier=self._settings.GENERATOR_ANOMALY_MULTIPLIER,
        )
        expected = expected_orders(
            self._settings.GENERATOR_ORDERS_PER_BATCH,
            factors,
        )
        order_count = sample_order_count(expected, self._count_rng)
        items: list[OrderItem] = []

        if order_count > 0:
            items = generate_orders(
                count=order_count,
                users=self._users,
                products=self._products,
                rng=self._order_rng,
                now=now,
            )
            self._repository.add_many(items)

        logger.info(
            "generated %d orders (%d items; expected %.2f)",
            order_count,
            len(items),
            expected,
        )
        return OrderBatchResult(
            expected_orders=expected,
            order_count=order_count,
            item_count=len(items),
        )

    def _log_anomaly_window(self) -> None:
        start = self._settings.GENERATOR_ANOMALY_START
        if start is None:
            logger.info("anomaly window disabled")
            return

        end = start + timedelta(
            minutes=self._settings.GENERATOR_ANOMALY_DURATION_MINUTES
        )
        logger.info(
            "anomaly window %s to %s (multiplier %.2f)",
            start.isoformat(),
            end.isoformat(),
            self._settings.GENERATOR_ANOMALY_MULTIPLIER,
        )
