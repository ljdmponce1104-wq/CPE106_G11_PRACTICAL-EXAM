# Concert Ticket Tracking System

Mapúa University — Software Design Laboratory Practical Exam

## Group 11
- Endriga, Christopher Mikel
- Marquez, Sebastian
- Ponce, Lawrence Jacob
- Somera, John Dylan

Section: CPE106L-4_B3

## System
A small-scale Concert Ticket Tracking / Queue Management System using generic test events.

The GUI uses the provided ticket-site screenshots as a visual reference for:
- navy / teal / white color palette
- top navigation/header
- event selection
- generic test-event information cards
- ticket-request area
- queue-management area

The application is an original classroom project and does not require an internet connection.

## 3-Tier Architecture
1. Presentation Layer — `presentation/main.py`
2. Business Logic Layer — `business/ticket_service.py`
3. Data Access Layer — `data/ticket_repository.py` and `data/database.py`

SQLite is used for persistent storage.

## Valid-choice rule
The selected event controls which ticket types are available. The business layer validates the event/ticket-type combination again before inserting it into SQLite. The GUI therefore does not rely only on visual dropdown restrictions.

## FIFO
Waiting requests are served by ascending queue number. The repository explicitly selects:
`ORDER BY queue_number ASC LIMIT 1`

## Minimum required features
- Search function
- Data validation
- User-friendly interface
- FIFO queue processing

## How to run
Requires Python 3.x. No third-party Python packages are required.

From the project folder:

```bash
python presentation/main.py
```

The SQLite database is created automatically if it does not exist.

## Formal testing
The practical exam requires notifying the instructor when it is time to perform testing. Follow that requirement before the formal test demonstration.

## Submission
- Project Documentation (PDF)
- Source Code
- SQLite Database
- Group Selfie


## Input Validation
The system only accepts valid ticket requests:
- Customer name: letters, spaces, periods, apostrophes, and hyphens.
- Contact number: Philippine format such as `09171234567` or `+639171234567`.
- Event: must be selected from the predefined event list.
- Ticket type: must belong to the selected event.
- Quantity: whole number from 1 to 10.

Invalid input is rejected before anything is inserted into SQLite.
