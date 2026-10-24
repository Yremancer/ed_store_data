import logging
import signal
import threading

from src.config import get_settings
from src.logger import setup_logging

logger = logging.getLogger(__name__)
settings = get_settings()

stop_event = threading.Event()


def stop(signum, _frame):
    logger.info("got signal %s, stopping...", signum)
    stop_event.set()


def main():
    setup_logging(settings.LOG_LEVEL)

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)

    logger.info("started")

    while not stop_event.is_set():
        stop_event.wait(5)
    logger.info("stopped")


if __name__ == "__main__":
    main()
