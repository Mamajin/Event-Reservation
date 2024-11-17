from django.test import TestCase
from django.utils import timezone
from api.models import AttendeeUser, Organizer, Event, Ticket
from datetime import datetime
from ninja.testing import TestClient
from ninja_jwt.tokens import RefreshToken
from faker import Faker
from django.conf import settings
from api.urls import api
from google.oauth2 import id_token
from google.auth.transport import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from botocore.exceptions import ClientError
from django.contrib.auth import get_user_model
import base64
import json

faker = Faker()

class UserModelsTest(TestCase):
    client = TestClient(api)

    def setUp(self):
        """
        Set up initial test data for models.
        """
        self.user_create_url = '/register'
        self.user_login_url = '/login'
        self.user_profile_url = '/profile'
        self.google_auth_url = '/auth/google'
        self.edit_user_url = '/edit-profile/'
        self.delete_user_url = 'delete/'
        self.upload_image_user_url = '/upload/profile-picture/'
        self.test_user = AttendeeUser.objects.create_user(
            username='attendeeuser3',
            password='password123',
            first_name='Jane',
            last_name='Doe',
            birth_date='1995-06-15',
            phone_number='9876543210',
            email='jane.doe@example.com'
        )

        
        # Create a mock JWT token structure
        self.header = {
            "alg": "RS256",
            "kid": "mock_key_id",
            "typ": "JWT"
        }
        
        self.payload = {
            "iss": "accounts.google.com",
            "azp": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            "aud": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            "sub": "12345678901234567890",
            "email": "test@example.com",
            "email_verified": True,
            "given_name": "Test",
            "family_name": "User",
            "name": "Test User",
            "picture": "https://example.com/photo.jpg",
            "locale": "en",
            "iat": 1616161616,
            "exp": 1616165216
        }

        # Create mock JWT token
        header_bytes = base64.urlsafe_b64encode(json.dumps(self.header).encode()).rstrip(b'=')
        payload_bytes = base64.urlsafe_b64encode(json.dumps(self.payload).encode()).rstrip(b'=')
        signature_bytes = base64.urlsafe_b64encode(b"mock_signature").rstrip(b'=')
        
        self.mock_token = f"{header_bytes.decode()}.{payload_bytes.decode()}.{signature_bytes.decode()}"
        
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
    
    def create_user(self, username, first_name, email):
        user = AttendeeUser.objects.create(
            username = username, 
            first_name = first_name,
            last_name = 'Doe',
            birth_date='1995-06-15',
            phone_number='9876543210',
            email= str(email) +'@example.com'
        )
        user.set_password("password123")
        user.save()
        return user
        
            
        