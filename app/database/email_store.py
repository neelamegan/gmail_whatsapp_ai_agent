
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "processed_emails.db"


def get_connection():
    """Create the data folder and connect to SQLite."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS processed_emails (
            email_id TEXT PRIMARY KEY,
            subject TEXT NOT NULL,
            importance TEXT NOT NULL,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    return connection


def is_processed(email_id: str) -> bool:
    """Return True if this email has already been processed."""
    with get_connection() as connection:
        row = connection.execute(
            "SELECT 1 FROM processed_emails WHERE email_id = ?",
            (email_id,),
        ).fetchone()

    return row is not None


def mark_processed(email_id: str, subject: str, importance: str):
    """Save the email ID so it will not be processed again."""
    with get_connection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO processed_emails
                (email_id, subject, importance)
            VALUES (?, ?, ?)
            """,
            (email_id, subject, importance),
        )


if __name__ == "__main__":
    with get_connection() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM processed_emails"
        ).fetchone()[0]

    print("SQLite database:", DB_PATH)
    print("Emails already processed:", count)
