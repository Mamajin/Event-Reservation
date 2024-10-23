from django.test import TestCase
from django.utils import timezone
from api.models import AttendeeUser, Organizer, Event, Ticket
from datetime import datetime
from ninja.testing import TestClient
from api.urls import user_router

class BaseModelsTest(TestCase):

    def setUp(self):
        """
        Set up initial test data for models.
        """
        self.client = TestClient(user_router)
        self.user_create_url = '/register'
        self.user_login_url = '/login'
        self.user_profile_url = '/profile'
        
        
        
        