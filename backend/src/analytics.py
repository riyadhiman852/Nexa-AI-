import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "nexa_analytics.db"


def init_analytics_db():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS call_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            call_id TEXT,
            timestamp TEXT NOT NULL,
            channel TEXT NOT NULL,
            outcome TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def record_call(call_id, channel, outcome):
    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        """
        INSERT INTO call_analytics
        (call_id, timestamp, channel, outcome)
        VALUES (?, ?, ?, ?)
        """,
        (
            call_id,
            datetime.now().isoformat(),
            channel,
            outcome,
        ),
    )

    conn.commit()
    conn.close()


def get_call_stats():
    conn = sqlite3.connect(DB_PATH)

    total = conn.execute(
        "SELECT COUNT(*) FROM call_analytics"
    ).fetchone()[0]

    successful = conn.execute(
        "SELECT COUNT(*) FROM call_analytics WHERE outcome = 'success'"
    ).fetchone()[0]

    failed = conn.execute(
        "SELECT COUNT(*) FROM call_analytics WHERE outcome = 'failed'"
    ).fetchone()[0]

    conn.close()

    return {
        "total": total,
        "successful": successful,
        "failed": failed,
    }