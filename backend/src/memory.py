import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "nexa_memory.db"


def init_db():
    """Create the memory database and users table if they don't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                language_preference TEXT,
                facts TEXT NOT NULL DEFAULT '{}',
                last_interaction TEXT NOT NULL
            )
            """
        )
        conn.commit()


def get_user(user_id: str):
    """Return a saved user record or None."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        row = conn.execute(
            """
            SELECT user_id, name, language_preference, facts, last_interaction
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

        if row is None:
            return None

        return {
            "user_id": row["user_id"],
            "name": row["name"],
            "language_preference": row["language_preference"],
            "facts": json.loads(row["facts"] or "{}"),
            "last_interaction": row["last_interaction"],
        }


def save_user(
    user_id: str,
    name: str,
    language_preference: str,
    facts: dict,
):
    """Create or update a user's memory."""
    now = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO users (
                user_id,
                name,
                language_preference,
                facts,
                last_interaction
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                name = excluded.name,
                language_preference = excluded.language_preference,
                facts = excluded.facts,
                last_interaction = excluded.last_interaction
            """,
            (
                user_id,
                name,
                language_preference,
                json.dumps(facts),
                now,
            ),
        )
        conn.commit()


init_db()