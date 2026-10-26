import logging

from app.gmail.gmail_reader import get_new_emails
from app.ai.email_classifier import classify_email
from app.tools.notification_tool import send_whatsapp_notification
from app.database.email_store import (
    is_processed,
    mark_processed,
)
from app.config import (
    MAX_EMAILS_PER_CHECK,
    OLLAMA_MODEL,
)

logger = logging.getLogger(__name__)


def run_agent():
    logger.info("Starting agent cycle")

    emails = get_new_emails(
        max_results=MAX_EMAILS_PER_CHECK
    )

    if not emails:
        logger.info("No unread emails found")
        return

    logger.info("Found %d unread emails", len(emails))

    for email in emails:
        email_id = email["id"]
        subject = email["subject"]

        if is_processed(email_id):
            logger.info("Already processed; skipping: %s", subject)
            continue

        logger.info("Analyzing email: %s", subject)

        try:
            result = classify_email(email)
            importance = result["importance"]
            summary = result["summary"]

            logger.info(
                "Classification: %s | Category: %s",
                importance,
                result.get("category", "unknown"),
            )

            if importance == "important":
                send_whatsapp_notification(
                    subject=subject,
                    summary=summary,
                )
                logger.info(
                    "Notification simulator completed: %s",
                    subject,
                )
            else:
                logger.info(
                    "Normal email; notification skipped: %s",
                    subject,
                )

            mark_processed(
                email_id,
                subject,
                importance,
            )

        except Exception:
            logger.exception(
                "Failed to process email: %s",
                subject,
            )

    logger.info("Agent cycle completed")


if __name__ == "__main__":
    from app.logging_config import setup_logging

    setup_logging()
    run_agent()