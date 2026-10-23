# EventHub — Django REST Framework API

EventHub is a simplified event ticketing API built using Django and Django REST Framework. It supports event browsing, filtering events, reserving seats, cancelling reservations, and request logging.

## Requirements

- Python 3.10+
- pip
- Postman (for API testing)

## Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Create database migrations

```bash
python manage.py makemigrations events
python manage.py migrate
```

### 4. Start the development server

```bash
python manage.py runserver
```

Open the browsable API at:

http://127.0.0.1:8000/api/

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/events/` | List all events |
| POST | `/api/events/` | Create an event |
| GET | `/api/events/{id}/` | Retrieve an event |
| PUT/PATCH | `/api/events/{id}/` | Update an event |
| DELETE | `/api/events/{id}/` | Delete an event |
| GET | `/api/events/?status=upcoming` | Filter events by status |
| GET | `/api/events/?venue=nimhans` | Filter events by venue |
| GET | `/api/reservations/` | List reservations |
| POST | `/api/reservations/` | Create a reservation |
| GET | `/api/reservations/{id}/` | Retrieve a reservation |
| PUT/PATCH | `/api/reservations/{id}/` | Update a reservation |
| DELETE | `/api/reservations/{id}/` | Delete a reservation |
| GET | `/api/reservations/?event_id=1` | Filter reservations by event |
| POST | `/api/reservations/{id}/cancel/` | Cancel a reservation and restore seats |

## Example Requests

### Create an Event

**POST** `/api/events/`

```json
{
  "title": "PyCon India",
  "venue": "NIMHANS Convention Centre, Bangalore",
  "date": "2027-09-20",
  "total_seats": 500,
  "available_seats": 500,
  "status": "upcoming"
}
```

### Reserve Seats

**POST** `/api/reservations/`

```json
{
  "event": 1,
  "attendee_name": "Priya Sharma",
  "attendee_email": "priya@example.com",
  "seats_reserved": 2
}
```

On successful reservation, the API returns `201 Created` and deducts the reserved seats from the event's available seats.

### Cancel a Reservation

**POST** `/api/reservations/1/cancel/`

No request body is required.

A successful cancellation marks the reservation as cancelled, restores its seats, and returns `200 OK`.

## Design Decision

The reservation creation logic updates the event's available seat count and creates the reservation within a database transaction. This helps keep the two database changes consistent if an operation fails. Row-level locking is used where supported to help protect against concurrent bookings.

## Request Logging Middleware

The custom `RequestLoggingMiddleware` records the HTTP method, request path, response status code, and request processing time. The log messages appear in the terminal where the Django development server is running.

## Postman Screenshots

The following screenshots are included as part of the assignment submission:

1. `screenshots/successful_reservation.png` — Successful reservation (`201 Created`).
2. `screenshots/overbooking_failure.png` — Overbooking rejected (`400 Bad Request`).
3. `screenshots/successful_cancellation.png` — Successful cancellation (`200 OK`).

## GitHub Submission Checklist

- Include all source code in the correct files.
- Include the generated Django migrations.
- Include the three required Postman screenshots.
- Include this README file.
- Do not commit the virtual environment (`venv/`) or local database (`db.sqlite3`).
- Push the project to a public GitHub repository.
