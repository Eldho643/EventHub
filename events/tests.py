from datetime import date
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Event, Reservation


class EventHubAPITests(APITestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title="Test Event",
            venue="Test Venue",
            date=date(2027, 9, 20),
            total_seats=3,
            available_seats=3,
            status="upcoming",
        )

    def test_create_reservation_deducts_seats(self):
        response = self.client.post(
            "/api/reservations/",
            {
                "event": self.event.id,
                "attendee_name": "Test Attendee",
                "attendee_email": "test@example.com",
                "seats_reserved": 2,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.event.refresh_from_db()
        self.assertEqual(self.event.available_seats, 1)

    def test_overbooking_is_rejected(self):
        response = self.client.post(
            "/api/reservations/",
            {
                "event": self.event.id,
                "attendee_name": "Test Attendee",
                "attendee_email": "test@example.com",
                "seats_reserved": 4,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancellation_restores_seats(self):
        reservation = Reservation.objects.create(
            event=self.event,
            attendee_name="Test Attendee",
            attendee_email="test@example.com",
            seats_reserved=2,
        )
        self.event.available_seats = 1
        self.event.save()
        response = self.client.post(
            f"/api/reservations/{reservation.id}/cancel/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.available_seats, 3)
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, "cancelled")
