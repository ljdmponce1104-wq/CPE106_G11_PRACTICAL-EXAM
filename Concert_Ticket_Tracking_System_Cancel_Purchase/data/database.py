import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "concert_ticket_queue.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ticket_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                queue_number INTEGER NOT NULL UNIQUE,
                customer_name TEXT NOT NULL,
                contact_number TEXT NOT NULL,
                event_name TEXT NOT NULL,
                event_date TEXT NOT NULL,
                ticket_type TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                status TEXT NOT NULL DEFAULT 'Waiting'
                    CHECK(status IN ('Waiting', 'Served', 'Cancelled')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                processed_at TEXT
            )
        """)

        # Safe migration for an older database created by the first version.
        columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(ticket_queue)").fetchall()
        }
        if "event_date" not in columns:
            conn.execute(
                "ALTER TABLE ticket_queue ADD COLUMN event_date TEXT NOT NULL DEFAULT 'Not specified'"
            )

        conn.commit()
