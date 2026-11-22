import logging
import signal
import threading
from random import Random

from src.clock import utc_now
from src.config import get_settings
from src.database import create_client
from src.logger import setup_logging
from src.orders.repository import OrderRepository
from src.orders.service import OrderGenerationService
from src.products.repository import ProductRepository
from src.users.generator import generate_users
from src.users.repository import UserRepository

logger = logging.getLogger(__name__)


def main() -> None:
    settings = get_settings()
    setup_logging(settings.LOG_LEVEL)
    stop_event = threading.Event()

    def stop(signum, frame) -> None:
        del signum, frame
        stop_event.set()

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)

    logger.info("started")

    client = create_client(settings)
    try:
        user_repository = UserRepository(client)
        users = user_repository.get_all()
        if not users:
            users = generate_users(
                count=settings.GENERATOR_USERS_COUNT,
                rng=Random(settings.GENERATOR_SEED),
                now=utc_now().replace(microsecond=0),
            )
            user_repository.add_many(users)
            logger.info("created %d users", len(users))
        else:
            logger.info("loaded %d existing users", len(users))

        products = ProductRepository(client).get_all()
        logger.info("loaded %d products", len(products))

        order_repository = OrderRepository(client)
        service = OrderGenerationService(
            settings=settings,
            users=users,
            products=products,
            repository=order_repository,
            stop_event=stop_event,
        )
        service.run()
        logger.info("stop requested")
    finally:
        client.close()
        logger.info("stopped")


if __name__ == "__main__":
    main()
