from .database import get_connection

class TicketRepository:
    """Data-access layer: all SQLite operations are kept here."""

    def get_next_queue_number(self):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT COALESCE(MAX(queue_number), 0) + 1 AS next_number "
                "FROM ticket_queue"
            ).fetchone()
            return row["next_number"]

    def add(self, customer_name, contact_number, event_name, event_date,
            ticket_type, quantity):
        queue_number = self.get_next_queue_number()
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO ticket_queue
                (queue_number, customer_name, contact_number, event_name,
                 event_date, ticket_type, quantity, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'Waiting')
            """, (
                queue_number, customer_name, contact_number, event_name,
                event_date, ticket_type, quantity
            ))
            conn.commit()
        return queue_number

    def process_next(self):
        """FIFO: serve the Waiting record with the smallest queue number."""
        with get_connection() as conn:
            row = conn.execute("""
                SELECT * FROM ticket_queue
                WHERE status = 'Waiting'
                ORDER BY queue_number ASC
                LIMIT 1
            """).fetchone()

            if row is None:
                return None

            conn.execute("""
                UPDATE ticket_queue
                SET status = 'Served', processed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (row["id"],))
            conn.commit()
            return dict(row)

    def cancel(self, queue_number):
        """Cancel a waiting purchase without deleting its history."""
        with get_connection() as conn:
            row = conn.execute("""
                SELECT * FROM ticket_queue
                WHERE queue_number = ?
            """, (queue_number,)).fetchone()

            if row is None:
                return None, "Ticket request was not found."

            if row["status"] != "Waiting":
                return dict(row), "Only waiting purchases can be cancelled."

            conn.execute("""
                UPDATE ticket_queue
                SET status = 'Cancelled', processed_at = CURRENT_TIMESTAMP
                WHERE queue_number = ?
            """, (queue_number,))
            conn.commit()

            updated = conn.execute("""
                SELECT * FROM ticket_queue
                WHERE queue_number = ?
            """, (queue_number,)).fetchone()

            return dict(updated), None

    def search(self, keyword="", status="All"):
        keyword = keyword.strip()
        like = f"%{keyword}%"

        with get_connection() as conn:
            if status == "All":
                rows = conn.execute("""
                    SELECT * FROM ticket_queue
                    WHERE CAST(queue_number AS TEXT) LIKE ?
                       OR customer_name LIKE ?
                       OR contact_number LIKE ?
                       OR event_name LIKE ?
                       OR event_date LIKE ?
                       OR ticket_type LIKE ?
                    ORDER BY queue_number ASC
                """, (like, like, like, like, like, like)).fetchall()
            else:
                rows = conn.execute("""
                    SELECT * FROM ticket_queue
                    WHERE status = ?
                      AND (
                        CAST(queue_number AS TEXT) LIKE ?
                        OR customer_name LIKE ?
                        OR contact_number LIKE ?
                        OR event_name LIKE ?
                        OR event_date LIKE ?
                        OR ticket_type LIKE ?
                      )
                    ORDER BY queue_number ASC
                """, (status, like, like, like, like, like, like)).fetchall()

            return [dict(row) for row in rows]

    def get_waiting_count(self):
        with get_connection() as conn:
            return conn.execute(
                "SELECT COUNT(*) AS count FROM ticket_queue WHERE status='Waiting'"
            ).fetchone()["count"]

    def clear_all(self):
        with get_connection() as conn:
            conn.execute("DELETE FROM ticket_queue")
            conn.commit()
