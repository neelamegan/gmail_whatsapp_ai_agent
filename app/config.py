import os

from dotenv import load_dotenv

load_dotenv()

POLL_INTERVAL_SECONDS = int(
    os.getenv("POLL_INTERVAL_SECONDS", "60")
)

MAX_EMAILS_PER_CHECK = int(
    os.getenv("MAX_EMAILS_PER_CHECK", "5")
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL", "qwen2.5:3b"
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL", "INFO"
).upper()

if POLL_INTERVAL_SECONDS < 10:
    raise ValueError(
        "POLL_INTERVAL_SECONDS must be at least 10."
    )

if MAX_EMAILS_PER_CHECK < 1:
    raise ValueError(
        "MAX_EMAILS_PER_CHECK must be at least 1."
    )

if LOG_LEVEL not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
    raise ValueError("Invalid LOG_LEVEL in .env.")