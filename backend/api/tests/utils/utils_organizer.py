from django.test import TestCase
from django.utils import timezone
from api.models import AttendeeUser, Organizer, Event, Ticket
from datetime import datetime
from ninja.testing import TestClient
from api.urls import api
from ninja_jwt.tokens import RefreshToken
from faker import Faker
from unittest.mock import patch, Mock, MagicMock
from django.core.files.uploadedfile import SimpleUploadedFile
from botocore.exceptions import ClientError
import datetime
from django.utils import timezone

ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg']
fake = Faker()

class OrganizerModelsTest(TestCase):
    EXCEED_SIZE = 10 * 1024 * 1024

    def setUp(self):
        client = TestClient(api)
        """
        Set up initial test data for models.
        """
        
        self.apply_organizer_url = '/api/organizers/apply-organizer'
        self.delete_event_url = f"/api/organizers/delete-event/"
        self.update_organizer_url = '/api/organizers/update-organizer'
        self.revoke_organizer_url = '/api/organizers/revoke-organizer'
        self.view_organizer_url = "/api/organizers/view-organizer"
        self.upload_logo_organizer_url = '/api/organizers/upload/logo/'
        self.test_user = AttendeeUser.objects.create_user(
            username='attendeeuser3',
            password='password123',
            first_name='Jane',
            last_name='Doe',
            birth_date='1995-06-15',
            phone_number='9876543210',
            email='jane.doe@example.com'
        )
        
        self.event_test = Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user", "test"),
            start_date_event=timezone.now(),
            end_date_event= timezone.now() + datetime.timedelta(days = 1),  # Ensure it ends after it starts
            start_date_register=timezone.now() - datetime.timedelta(days = 2),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 3),  # Registration ends when the event starts
            max_attendee=fake.random_int(min=10, max=500),
            description=fake.text(max_nb_chars=200),
        )
        
    def get_token_for_user(self, user):
        """Helper method to generate a JWT token for the test user"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def become_organizer(self,user, organizer_name, email):
        organizer = Organizer.objects.create(
            user= user,
            organizer_name = organizer_name,
            email = str(email) + "@example.com",
            organization_type = "INDIVIDUAL",
            logo = fake.file_name()
        )
        return organizer

    
    def create_user(self, username, first_name, email):
        return AttendeeUser.objects.create_user(
            username = username, 
            password = "password123",
            first_name = first_name,
            last_name = 'Doe',
            birth_date='1995-06-15',
            phone_number='9876543210',
            email= str(email)+'.doe@example.com'
        )
          
        