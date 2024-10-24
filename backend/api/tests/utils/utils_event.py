from django.test import TestCase
from django.utils import timezone
from api.models import AttendeeUser, Organizer, Event, Ticket
from datetime import datetime
from ninja.testing import TestClient
from api.urls import event_router
from ninja_jwt.tokens import RefreshToken
from faker import Faker
import datetime
from django.utils import timezone

fake = Faker()

class EventModelsTest(TestCase):

    def setUp(self):
        """
        Set up initial test data for models.
        """
        self.client = TestClient(event_router)
        self.event_create_url = '/create-event'
        self.user_login_url = '/login'
        self.user_profile_url = '/profile'
        self.test_user = AttendeeUser.objects.create(
            username='attendeeuser4',
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
            start_date_event=timezone.make_aware(fake.date_time_this_year()),
            end_date_event=timezone.make_aware(fake.date_time_this_year() + datetime.timedelta(days=1)),  # Ensure it ends after it starts
            start_date_register=timezone.make_aware(fake.date_time_this_year() - datetime.timedelta(days=5)),  # Example for registration start
            end_date_register=timezone.make_aware(fake.date_time_this_year()),  # Registration ends when the event starts
            max_attendee=fake.random_int(min=10, max=500),
            description=fake.text(max_nb_chars=200)
        )
        
        self.token = self.get_token_for_user(self.test_user)
        
        self.organizer = self.become_organizer(self.test_user, "test_user")
        

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
    
    
        