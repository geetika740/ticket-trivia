from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Monument, Booking

class MonumentModelTest(TestCase):
    def setUp(self):
        Monument.objects.create(
            name="Red Fort",
            description="Historic fort in Delhi",
            location="Delhi",
            price_per_ticket=100.00,
            category="Monument",
            image="monuments/redfort.jpg"
        )

    def test_monument_str(self):
        monument = Monument.objects.get(name="Red Fort")
        self.assertEqual(str(monument), "Red Fort")

class BookingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.monument = Monument.objects.create(
            name="Taj Mahal",
            description="Famous monument",
            location="Agra",
            price_per_ticket=200.00,
            category="Monument",
            image="monuments/taj.jpg"
        )

    def test_booking_creation(self):
        booking = Booking.objects.create(
            user=self.user,
            monument=self.monument,
            date="2025-08-01",
            num_tickets=2,
            total_amount=400.00,
            payment_status=True
        )
        self.assertEqual(str(booking), "testuser - Taj Mahal on 2025-08-01")

class UserAuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="sampleuser", password="samplepass")

    def test_login(self):
        login = self.client.login(username="sampleuser", password="samplepass")
        self.assertTrue(login)
