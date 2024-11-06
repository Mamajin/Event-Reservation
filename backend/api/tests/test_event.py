from .utils.utils_event import EventModelsTest, timezone,datetime, Event, Organizer, fake, patch, ALLOWED_IMAGE_TYPES, MagicMock, ClientError, SimpleUploadedFile

from django.http import QueryDict
import tempfile
import json
class EventTest(EventModelsTest):

    def test_organizer_create_event(self):
    # Prepare user and token
        user = self.create_user("become_organizer", "become_organizer")
        token = self.get_token_for_user(user)
        organizer = self.become_organizer(user, "become_organizer")

        # Create an image file for testing
        
        image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'some content',
            content_type='image/png'
        )

        # Prepare event data
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
            "latitude": "0.0",
            "longitude": "0.0",
            "is_free": "true",
            "ticket_price": "0.00",
            "expected_price": "0.00",
            "detailed_description": "Join us for an exciting event!",
            "contact_email": "info@techconference.com",
            "contact_phone": "+1234567890",
            "updated_at": timezone.now().isoformat()
        }

        # Make the request
        response = self.client.post(
            self.event_create_url,
            data= data,
            FILES = {'image': image_file},# Combine data and file
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {token}'}  # Use HTTP_AUTHORIZATION instead of headers
        )

        
        # Check the response content
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Event.objects.filter(event_name="Annual Tech Conference").exists())
        
        # Verify image upload


            
    def test_invalid_image_create_event(self):
        # Prepare user and token
        user = self.create_user("become_organizer", "become_organizer")
        token = self.get_token_for_user(user)
        organizer = self.become_organizer(user, "become_organizer")

        # Create an image file for testing
        image = SimpleUploadedFile(
            name='test_image.gif',
            content=b'',  # Empty content for testing
            content_type='image/gif'
        )
        


        # Prepare event data
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
            
        response = self.client.post(
            self.event_create_url,
            data= data,
            FILES = {'image': image },
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        # Make the request with multipart/form-data for the image upload
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json()['error'], 'Invalid file type. Only JPEG and PNG are allowed.')
        
        
        
    def test_user_cannot_create_event(self):
        just_user = self.create_user("not_organizer", "not_organizer")
        token  = self.get_token_for_user(just_user)
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
        
        self.assertFalse(Organizer.objects.filter(user = just_user).exists())
        response = self.client.post(
            self.event_create_url,
            data= data,  
            content_type='multipart/form-data',  # Ensure the correct content type
            headers={'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], "You are not an organizer.")
        
    
    def test_date_input_invalid(self):
        data = {
            "category": "CONFERENCE",
            "dress_code": "CASUAL",
            "event_name": "Annual Tech Conference",
            "event_create_date": timezone.now().isoformat(),
            "start_date_event": (timezone.now() + datetime.timedelta(days=2)).isoformat(),
            "end_date_event": (timezone.now() + datetime.timedelta(days=3)).isoformat(),
            "start_date_register": timezone.now().isoformat(),
            "end_date_register": (timezone.now() - datetime.timedelta(days=3)).isoformat(),
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
        normal_user = self.create_user("test", "test")
        organizer = self.become_organizer(normal_user, "test")
        token  = self.get_token_for_user(normal_user)
        response = self.client.post(
            self.event_create_url,
            data= data,  # Wrap the data in a 'data' key
            content_type='multipart/form-data',  # Ensure the correct content type
            headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter valid date', response.json().get("error", ""))
        
    
    @patch('boto3.client')
    def test_s3_upload_failure(self, mock_boto3_client):
        """Test handling of S3 upload failure"""
        # Setup
        user = self.create_user("become_organizer", "become_organizer")
        token = self.get_token_for_user(user)
        organizer = self.become_organizer(user, "become_organizer")
        
        # Mock S3 client to raise ClientError
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3
        mock_s3.upload_fileobj.side_effect = ClientError(
            error_response={'Error': {'Message': 'S3 Upload Failed'}},
            operation_name='upload_fileobj'
        )

        # Prepare request data
        event_data = self.get_valid_data()
        image_file = self.create_test_image()

        # Make request
        response = self.client.post(
            self.event_create_url,
            data=event_data,
            FILES={'image': image_file},
            headers={'Authorization': f'Bearer {token}'}
        )


        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertIn('S3 upload failed', response.json()['error'])
        
        # Verify the event was not created
        self.assertFalse(Event.objects.filter(event_name=event_data['event_name']).exists())


    def test_invalid_organizer_get_my_events(self):
        normal_user  = self.create_user("test","test")
        token = self.get_token_for_user(normal_user)
        response = self.client.get(self.organizer_get_events, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 404)
        response1 = self.client.get(self.organizer_get_events)
        
        
    def test_valid_organizer_get_my_events(self):
        normal_user  = self.create_user("test","test")
        organizer = self.become_organizer(normal_user,"test")
        token = self.get_token_for_user(normal_user)
        response = self.client.get(self.organizer_get_events, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        
        
    def test_valid_get_my_events(self):
        token = self.get_token_for_user(self.test_user)
        response = self.client.get(self.organizer_get_events, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        
    @patch("api.models.Event.objects.filter")
    def test_exception_get_my_events(self, mock_filter):
        mock_filter.side_effect = Exception("Unexpected error occurred")
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        organizer = self.become_organizer(user, "test")

        # Simulate a GET request to the /my-events endpoint
        response = self.client.get(self.organizer_get_events, headers={'Authorization': f'Bearer {token}'})

        # Check that the response status code is 400
        self.assertEqual(response.status_code, 400)
        print(response.json())

        # Check that the response contains the correct error message
        self.assertEqual(response.json(), {'error': 'Unexpected error occurred'})


        
        
    # def test_can_register(self):
    #     event_test = Event.objects.create(
    #         event_name=fake.company(),
    #         organizer= self.become_organizer(self.test_user, "test_user"),
    #         start_date_register=timezone.now() - datetime.timedelta(days = 2),  # Example for registration start
    #         end_date_register=timezone.now() + datetime.timedelta(days = 1),  # Registration ends when the event starts
    #         start_date_event=timezone.now() + datetime.timedelta(days = 3),
    #         end_date_event= timezone.now() + datetime.timedelta(days = 4),  # Ensure it ends after it starts
    #         max_attendee=fake.random_int(min=10, max=500),
    #         description=fake.text(max_nb_chars=200)
    #     )
    #     self.assertTrue(event_test.can_register())
        
    # def test_date_input_is_valid(self):
    #     event_data = {
    #         'event_name': 'Annual Tech Conference',
    #         'start_date_register': timezone.now(),                    # Registration starts now
    #         'end_date_register': timezone.now() + datetime.timedelta(days=1), # Registration ends in 5 days
    #         'start_date_event': timezone.now() + datetime.timedelta(days=2),  # Start tomorrow
    #         'end_date_event': timezone.now() + datetime.timedelta(days=3),    # End the day after
    #         'description': 'A tech event for showcasing new innovations.',
    #         'max_attendee': 100
    #     }
    #     normal_user = self.create_user("test", "test")
    #     organizer = self.become_organizer(normal_user, "test")
    #     token  = self.get_token_for_user(normal_user)
    #     response = self.client.post(self.event_create_url, json=event_data, headers={'Authorization': f'Bearer {token}'})
    #     self.assertEqual(response.status_code, 200)
        

        
        
    # def test_valid_get_all_events(self):
    #     response = self.client.get(self.list_event_url)
    #     self.assertEqual(response.status_code, 200)
        
    # def test_valid_get_event_detail(self):
    #     response = self.client.get(self.get_event_detail_url + str(self.event_test.id))
    #     self.assertEqual(response.status_code, 200)
        
        
    # def test_valid_edit_event(self):
    #     new_data = {
    #         "event_name": fake.company(),
    #         "start_date_register": timezone.now() - datetime.timedelta(days = 2),
    #         "end_date_register": timezone.now() - datetime.timedelta(days = 1),
    #         "start_date_event": timezone.now(),
    #         "end_date_event": timezone.now() + datetime.timedelta(days = 1),
    #         "max_attendee": 1,
    #         "description": fake.text(max_nb_chars=200)
    #     }
    #     token = self.get_token_for_user(self.test_user)
        
    #     response = self.client.put(self.edit_event_url + str(self.event_test.id), json = new_data ,headers={'Authorization': f'Bearer {token}'})
    #     self.assertEqual(response.status_code, 204)
        
        
    # def test_invalid_organizer_edit_event(self):
    #     new_data = {
    #         "event_name": fake.company(),
    #         "start_date_register": timezone.now() - datetime.timedelta(days = 2),
    #         "end_date_register": timezone.now() - datetime.timedelta(days = 1),
    #         "start_date_event": timezone.now(),
    #         "end_date_event": timezone.now() + datetime.timedelta(days = 1),
    #         "max_attendee": 1,
    #         "description": fake.text(max_nb_chars=200)
    #     }
    #     normal_user = self.create_user("test","test")
    #     token = self.get_token_for_user(normal_user)
    #     response = self.client.put(self.edit_event_url + str(self.event_test.id), json = new_data ,headers={'Authorization': f'Bearer {token}'})
    #     self.assertEqual(response.status_code, 404)
    #     normal_user1  = self.create_user("test1","test1")
    #     organizer = self.become_organizer(normal_user1, "test_organizer")
    #     token1 = self.get_token_for_user(normal_user1)
    #     response = self.client.put(self.edit_event_url + str(self.event_test.id), json = new_data ,headers={'Authorization': f'Bearer {token1}'})
    #     self.assertIn('You are not allowed to edit this event.', response.json().get("error", ""))
    #     self.assertTrue(response.status_code, 403)
        
        
    # def test_edit_does_not_exist(self):
    #     normal_user = self.create_user("test","test")
    #     token = self.get_token_for_user(normal_user)
    #     new_data = {
    #         "event_name": fake.company(),
    #         "start_date_register": timezone.now() - datetime.timedelta(days = 2),
    #         "end_date_register": timezone.now() - datetime.timedelta(days = 1),
    #         "start_date_event": timezone.now(),
    #         "end_date_event": timezone.now() + datetime.timedelta(days = 1),
    #         "max_attendee": 1,
    #         "description": fake.text(max_nb_chars=200)
    #     }
    #     response = self.client.put(self.edit_event_url + str(2), json = new_data ,headers={'Authorization': f'Bearer {token}'})
    #     self.assertTrue(response.status_code, 404)
    #     self.assertIn('Event not found', response.json().get("error", ""))
        
        
    # @patch("api.models.Organizer.objects.get")
    # def test_get_my_events_unexpected_exception(self, mock_get_organizer):
    #     # Mock Organizer.objects.get to raise an unexpected exception
    #     mock_get_organizer.side_effect = Exception(f"Error while retrieving events for organizer {self.test_user.id}")
    #     token = self.get_token_for_user(self.test_user)

    #     # Make the request with a JWT token in the header
    #     response = self.client.get(
    #         self.organizer_get_events,  # Replace with the actual URL name for your endpoint
    #         headers={'Authorization': f'Bearer {token}'}
    #     )
  
    #     # Assert that the response status is 400 (Bad Request)
    #     self.assertEqual(response.status_code,  400)

    #     # Assert that the response contains the error message
    #     self.assertEqual(response.data['error'], f"Error while retrieving events for organizer {self.test_user.id}")
        
    # @patch("api.models.Event.objects.filter")
    # def test_list_event_unexpected_exception(self,mock_filter):
    #         # Simulate a DatabaseError
    #     mock_filter.side_effect = Exception(f"Error while retrieving events for the homepage")

    #     response = self.client.get(self.list_event_url)
    #     self.assertEqual(response.status_code,400)
    #     self.assertIn(f"Error while retrieving events for the homepage", response.json().get("error", ""))
        
    # @patch("api.models.Event.objects.get")
    # def test_edit_evnt_unexpected_exception(self, mock_get_event):
    #     new_data = {
    #         "event_name": fake.company(),
    #         "start_date_register": timezone.now() - datetime.timedelta(days = 2),
    #         "end_date_register": timezone.now() - datetime.timedelta(days = 1),
    #         "start_date_event": timezone.now(),
    #         "end_date_event": timezone.now() + datetime.timedelta(days = 1),
    #         "max_attendee": 1,
    #         "description": fake.text(max_nb_chars=200)
    #     }
    #     mock_get_event.side_effect = Exception(f"Error while editing event {self.event_test.id}")
    #     token = self.get_token_for_user(self.test_user)
        
    #     response = self.client.put(self.edit_event_url + str(2), json = new_data ,headers={'Authorization': f'Bearer {token}'})
    #     self.assertEqual(response.status_code,400)
    #     self.assertIn(f"Error while editing event {self.event_test.id}", response.json().get("error", ""))
        

        
        
        
        
        

        
        
        
        
        
        
        
        

        
        

        
        

        

        
        
        

        
        
        

    


