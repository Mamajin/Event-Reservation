from django.test import TestCase
from django.utils import timezone
from api.models import AttendeeUser, Organizer, Event, Ticket
from datetime import datetime
from ninja.testing import TestClient
from api.urls import organizer_router
from ninja_jwt.tokens import RefreshToken
from faker import Faker
import datetime
from django.utils import timezone

fake = Faker()

class OrganizerModelsTest(TestCase):

    def setUp(self):
        """
        Set up initial test data for models.
        """
        
        self.client = TestClient(organizer_router)
        self.apply_organizer_url = '/apply-organizer'
        self.delete_event_url = f"/delete-event/"
        self.update_organizer_url = '/update-organizer'
        self.revoke_organizer_url = '/revoke-organizer'
        self.view_organizer_url = "/view-organizer"
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
            organizer= self.become_organizer(self.test_user, "test_user"),
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
    
    def become_organizer(self,user, organizer_name):
        self.organizer, created = Organizer.objects.get_or_create(
            user= user,
            organizer_name = organizer_name,
        )
        return self.organizer

    
    def create_user(self, username, first_name):
        return AttendeeUser.objects.create_user(
            username = username, 
            password = "password123",
            first_name = first_name,
            last_name = 'Doe',
            birth_date='1995-06-15',
            phone_number='9876543210',
            email='jane.doe@example.com'
        )
          
        