from dataclasses import dataclass
from typing import Optional

@dataclass
class TicketRequest:
    queue_number: Optional[int]
    customer_name: str
    contact_number: str
    event_name: str
    event_date: str
    ticket_type: str
    quantity: int
    status: str = "Waiting"
    created_at: Optional[str] = None
    processed_at: Optional[str] = None
