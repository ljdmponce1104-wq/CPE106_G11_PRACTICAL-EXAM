import re
from data.ticket_repository import TicketRepository


class TicketService:
    """Business-logic layer: validation and queue rules."""

    EVENTS = {
        "Test Concert 1": {
            "date": "November 14, 2026 • 7:00 PM",
            "venue": "Main Arena",
            "ticket_types": ("VIP", "Regular", "Balcony", "General Admission"),
        },
        "Test Concert 2": {
            "date": "December 05, 2026 • 6:00 PM",
            "venue": "Main Arena",
            "ticket_types": ("VIP", "Regular", "Balcony", "General Admission"),
        },
        "Test Movie 1": {
            "date": "November 21, 2026 • 2:00 PM",
            "venue": "Cinema Hall 1",
            "ticket_types": ("Premium", "Regular", "Student"),
        },
        "Test Movie 2": {
            "date": "December 12, 2026 • 5:00 PM",
            "venue": "Cinema Hall 2",
            "ticket_types": ("Premium", "Regular", "Student"),
        },
        "Test Event 1": {
            "date": "January 16, 2027 • 10:00 AM",
            "venue": "Community Hall",
            "ticket_types": ("VIP", "Regular", "General Admission"),
        },
        "Test Event 2": {
            "date": "January 30, 2027 • 3:00 PM",
            "venue": "Community Hall",
            "ticket_types": ("VIP", "Regular", "General Admission"),
        },
    }

    def __init__(self):
        self.repo = TicketRepository()

    def event_names(self):
        return tuple(self.EVENTS.keys())

    def get_event_info(self, event_name):
        return self.EVENTS.get(event_name)

    def validate_ticket(
        self,
        customer_name,
        contact_number,
        event_name,
        ticket_type,
        quantity,
    ):
        errors = []

        # Customer name validation.
        name = customer_name.strip()
        if not name:
            errors.append("Customer name is required.")
        elif len(name) < 2:
            errors.append("Customer name must contain at least 2 characters.")
        elif not re.fullmatch(r"[A-Za-z][A-Za-z .'-]*", name):
            errors.append(
                "Customer name may contain letters, spaces, periods, apostrophes, and hyphens only."
            )

        # Contact validation.
        contact = contact_number.strip()
        if not contact:
            errors.append("Contact number is required.")
        elif not re.fullmatch(r"(?:\+?[0-9][0-9\s()\-]{6,18}[0-9]|[0-9]{7,15})", contact):
            errors.append("Enter a valid contact number.")

        # Event validation.
        event_info = self.EVENTS.get(event_name)
        if event_info is None:
            errors.append("Please select a valid event.")

        # Ticket type validation.
        if event_info is not None and ticket_type not in event_info["ticket_types"]:
            errors.append("Please select a ticket type valid for the selected event.")

        # Quantity validation.
        try:
            qty = int(quantity)
            if qty < 1 or qty > 10:
                errors.append("Quantity must be a whole number from 1 to 10.")
        except (TypeError, ValueError):
            errors.append("Quantity must be a whole number from 1 to 10.")

        return errors

    def add_ticket(
        self,
        customer_name,
        contact_number,
        event_name,
        ticket_type,
        quantity,
    ):
        errors = self.validate_ticket(
            customer_name,
            contact_number,
            event_name,
            ticket_type,
            quantity,
        )

        if errors:
            return False, errors, None

        event_date = self.EVENTS[event_name]["date"]

        queue_number = self.repo.add(
            customer_name.strip(),
            contact_number.strip(),
            event_name,
            event_date,
            ticket_type,
            int(quantity),
        )

        return True, [], queue_number

    def process_next(self):
        return self.repo.process_next()

    def cancel_purchase(self, queue_number):
        """Cancel a waiting purchase while preserving the record."""
        try:
            queue_number = int(queue_number)
        except (TypeError, ValueError):
            return False, "Invalid queue number."

        record, error = self.repo.cancel(queue_number)

        if error:
            return False, error

        return True, record

    def search(self, keyword="", status="All"):
        return self.repo.search(keyword, status)

    def waiting_count(self):
        return self.repo.get_waiting_count()
