from django.test import TestCase
from django.utils import timezone
from api.models import AttendeeUser, Organizer, Event, Ticket
from datetime import datetime
from ninja.testing import TestClient
from api.urls import user_router
from ninja_jwt.tokens import AccessToken, RefreshToken

class BaseModelsTest(TestCase):

    def setUp(self):
        """
        Set up initial test data for models.
        """
        self.client = TestClient(user_router)
        self.user_create_url = '/register'
        self.user_login_url = '/login'
        self.user_profile_url = '/profile'
        self.test_user = AttendeeUser.objects.create_user(
            username='attendeeuser2',
            password='password123',
            first_name='Jane',
            last_name='Doe',
            birth_date='1995-06-15',
            phone_number='9876543210',
            email='jane.doe@example.com'
        )
        
        
        
        