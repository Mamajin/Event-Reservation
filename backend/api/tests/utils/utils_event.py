from django.test import TestCase
from django.utils import timezone
from api.models import AttendeeUser, Organizer, Event, Ticket
from datetime import datetime
from ninja.testing import TestClient
from api.views.schemas.event_schema import EventResponseSchema
from ninja_jwt.tokens import RefreshToken
from faker import Faker
import datetime
from django.utils import timezone
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from api.urls import api
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg']

fake = Faker()

class EventModelsTest(TestCase):
    client = TestClient(api)

    def setUp(self):
        """
        Set up initial test data for models.
        """ 
        self.event_create_url = '/create-event'
        self.organizer_get_events = '/my-events'
        self.list_event_url = '/events'
        self.get_event_detail_url = '/'
        self.edit_event_url = '/edit'
        self.upload_image_url = '/upload/event-image/'
        self.get_engagement_url = '/engagement'
        self.get_comment_url = '/comments'
        self.test_user = AttendeeUser.objects.create(
            username='attendeeuser4',
            password='password123',
            first_name='Jane',
            last_name='Doe',
            birth_date='1995-06-15',
            phone_number='9876543210',
            email='jane.doe@example.com'
        )
        self.test_user1 = AttendeeUser.objects.create(
            username='attendeeuser5',
            password='password123',
            first_name='Jane',
            last_name='Doe',
            birth_date='1995-06-15',
            phone_number='9876543210',
            email='jane123.doe@example.com'
        )
        
        self.event_test = Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user"),
            start_date_event=timezone.now(),
            end_date_event= timezone.now() + datetime.timedelta(days = 1),  # Ensure it ends after it starts
            start_date_register=timezone.now() - datetime.timedelta(days = 2),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 3),  # Registration ends when the event starts
            max_attendee=fake.random_int(min=10, max=500),
            description=fake.text(max_nb_chars=200),
            event_image = fake.file_name()
        )
        
        self.organizer1 = Organizer.objects.create(user = self.test_user1, organizer_name = "win", 
                                                    email = "test@example.com", 
                                                    organization_type = "INDIVIDUAL")
        
        self.public_event = Event.objects.create(
            event_name="Public Event",
            organizer= self.organizer1,
            start_date_event=timezone.now(),
            end_date_event=timezone.now(),
            start_date_register=timezone.now(),
            end_date_register=timezone.now(),
            visibility="PUBLIC",
        )
        
        self.private_event = Event.objects.create(
            event_name="Private Event",
            organizer= self.organizer1,
            start_date_event=timezone.now(),
            end_date_event=timezone.now(),
            start_date_register=timezone.now(),
            end_date_register=timezone.now(),
            visibility="PRIVATE",
            allowed_email_domains="example.com, ku.th"
        )
        
    

    def get_token_for_user(self, user):
        """Helper method to generate a JWT token for the test user"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def become_organizer(self,user, organizer_name):
        self.organizer, created = Organizer.objects.get_or_create(
            user= user,
            organizer_name = organizer_name,
            email = "test@exmaple.com",
            organization_type = 'INDIVIDUAL',
            description = "",
            facebook_url = "",
            twitter_handle = "",
            instagram_handle = "",
            youtube_channel = "",
            logo = fake.file_name()
        )
        return self.organizer
    
    def get_valid_data(self):
        data = {
            "category": "CONFERENCE",
            "dress_code": "CASUAL",
            "event_name": "Annual Tech Conference",
            "event_create_date": timezone.now().isoformat(),
            "start_date_event": (timezone.now() + datetime.timedelta(days=2)).isoformat(),
            "end_date_event": (timezone.now() + datetime.timedelta(days=3)).isoformat(),
            "start_date_register": timezone.now().isoformat(),
            "end_date_register": (timezone.now() + datetime.timedelta(days=1)).isoformat(),
            "description": "A tech event for showcasing new innovations.",
            "max_attendee": 100,
            "address": "Tech Park, Downtown",
            "latitude": 0.0,
            "longitude": 0.0,
            "is_free": True,
            "ticket_price": 0.00,
            "expected_price": 0.00,
            "detailed_description": "Join us for an exciting event!",
            "contact_email": "info@techconference.com",
            "contact_phone": "+1234567890",
            "updated_at": timezone.now().isoformat(),

        }
        return data
    
    def create_test_image(self):
        """Helper method to create a test image file"""
        return SimpleUploadedFile(
            name='test_image.png',
            content=b'some content',
            content_type='image/png'
        )

    
    def create_user(self, username, first_name):
        return AttendeeUser.objects.create_user(
            username = username, 
            password = "password123",
            first_name = first_name,
            last_name = 'Doe',
            birth_date='1995-06-15',
            phone_number='9876543210',
            email='jane1.doe@example.com'
        )
            
    
    def create_event(self, start_register, end_register , start_event, end_event):
        return Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user"),
            start_date_event= start_event,
            end_date_event= end_event,  # Ensure it ends after it starts
            start_date_register= start_register,  # Example for registration start
            end_date_register= end_register,  # Registration ends when the event starts
            max_attendee=fake.random_int(min=10, max=500),
            description=fake.text(max_nb_chars=200),
            event_image = fake.file_name()
        )
        
    
        