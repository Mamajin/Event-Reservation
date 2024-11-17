from django.test import TestCase
from django.utils import timezone
from api.models import AttendeeUser, Organizer, Event, Ticket
from unittest.mock import patch
from datetime import datetime
from ninja.testing import TestClient
from api.urls import api
from ninja_jwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from faker import Faker
from django.contrib.auth import get_user_model
import datetime

fake = Faker()

class TicketModelsTest(TestCase):
    client = TestClient(api)

    def setUp(self):
        """
        Set up initial test data for models.
        """
        self.user_list_event_url = "/api/tickets/user/"
        self.user_reserve_event_url = '/api/tickets/event/'
        self.user_cancel_event_url = '/api/tickets/'
        self.test_user = AttendeeUser.objects.create_user(
            username='attendeeuser3',
            password='password123',
            first_name='Jane',
            last_name='Doe',
            birth_date='1995-06-15',
            phone_number='9876543210',
            email='jane123.doe@example.com'
        )
        
        self.organizer = self.become_organizer(self.test_user, "test_user")
        self.event_test = Event.objects.create(
            event_name=fake.company(),
            organizer= self.organizer,
            start_date_event=timezone.now(),
            end_date_event= timezone.now() + datetime.timedelta(days = 1),  # Ensure it ends after it starts
            start_date_register=timezone.now() - datetime.timedelta(days = 2),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 3),  # Registration ends when the event starts
            max_attendee=fake.random_int(min=10, max=500),
            description=fake.text(max_nb_chars=200)
        )
        
    def get_token_for_user(self, user):
        """Helper method to generate a JWT token for the test user"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def become_organizer(self, user, name):
        self.organizer, created = Organizer.objects.get_or_create(
            user= user,
            organizer_name = name
        )
        return self.organizer
    
    def create_user(self, username, first_name):
        user = AttendeeUser.objects.create(
            username = username, 
            first_name = first_name,
            last_name = 'Doe',
            birth_date='1995-06-15',
            phone_number='9876543210',
            email='jane.doe@example.com'
        )
        user.set_password("password123")
        return  user
        
            
        