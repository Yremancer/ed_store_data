import logging
import signal
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Generator")

stop_event = threading.Event()


def stop(signum, _frame):
    logger.info("got signal %s, stopping...", signum)
    stop_event.set()


def main():
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)

    logger.info("started")
    while not stop_event.is_set():
        stop_event.wait(5)
    logger.info("stopped")


if __name__ == "__main__":
    main()
