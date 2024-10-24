from django.test import TestCase
from django.utils import timezone
from api.models import AttendeeUser, Organizer, Event, Ticket
from datetime import datetime
from ninja.testing import TestClient
from api.urls import user_router
from ninja_jwt.tokens import RefreshToken
from faker import Faker
from django.contrib.auth import get_user_model

faker = Faker()

class UserModelsTest(TestCase):

    def setUp(self):
        """
        Set up initial test data for models.
        """
        self.client = TestClient(user_router)
        self.user_create_url = '/register'
        self.user_login_url = '/login'
        self.user_profile_url = '/profile'
        self.test_user = AttendeeUser.objects.create_user(
            username='attendeeuser3',
            password='password123',
            first_name='Jane',
            last_name='Doe',
            birth_date='1995-06-15',
            phone_number='9876543210',
            email='jane.doe@example.com'
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
        
            
        