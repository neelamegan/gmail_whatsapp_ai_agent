import time
import logging
from datetime import datetime

from app.ai.email_agent import run_agent
from app.config import POLL_INTERVAL_SECONDS
from app.logging_config import setup_logging

logger = logging.getLogger(__name__)


def main():
    setup_logging()

    logger.info("Gmail WhatsApp AI Agent started")
    logger.info(
        "Polling interval: %s seconds",
        POLL_INTERVAL_SECONDS,
    )

    try:
        while True:
            logger.info(
                "Checking Gmail at %s",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

            try:
                run_agent()
            except Exception:
                logger.exception("Agent cycle failed")

            logger.info(
                "Waiting %s seconds for the next check",
                POLL_INTERVAL_SECONDS,
            )

            time.sleep(POLL_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        logger.info("Agent stopped by user")


if __name__ == "__main__":
    main()