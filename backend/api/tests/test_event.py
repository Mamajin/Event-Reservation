from .utils.utils_event import EventModelsTest, timezone,datetime, Event, Organizer, fake, patch, ALLOWED_IMAGE_TYPES, MagicMock, ClientError, SimpleUploadedFile,ValidationError, EventResponseSchema

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
            "updated_at": timezone.now().isoformat(),
            'image' : image_file
        }

        # Make the request
        response = self.client.post(
            path = '/api/events/create-event',
            data = data,
            headers={'Authorization': f'Bearer {token}'}  
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
            'image': image
        }
            
        response = self.client.post(
            path = '/api/events/create-event',
            data= data,
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
            path = '/api/events/create-event',
            data= data,
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
            path = '/api/events/create-event',
            data= data,  # Wrap the data in a 'data' key
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
        event_data['image'] = image_file

        # Make request
        response = self.client.post(
            path = '/api/events/create-event',
            data=event_data,
            headers={'Authorization': f'Bearer {token}'}
        )


        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertIn('S3 upload failed', response.json()['error'])
        
        # Verify the event was not created
        self.assertFalse(Event.objects.filter(event_name=event_data['event_name']).exists())
        
        

    # ## Test get_my_events function
    def test_invalid_organizer_get_my_events(self):
        normal_user  = self.create_user("test","test")
        token = self.get_token_for_user(normal_user)
        response = self.client.get('/api/events/my-events', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 404)
        response1 = self.client.get(self.organizer_get_events)
        
        
    def test_valid_organizer_get_my_events(self):
        normal_user  = self.create_user("test","test")
        organizer = self.become_organizer(normal_user,"test")
        token = self.get_token_for_user(normal_user)
        response = self.client.get('/api/events/my-events', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        
        
    def test_valid_get_my_events(self):
        token = self.get_token_for_user(self.test_user)
        response = self.client.get('/api/events/my-events', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        
    @patch("api.models.Event.objects.filter")
    def test_exception_get_my_events(self, mock_filter):
        mock_filter.side_effect = Exception("Unexpected error occurred")
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        organizer = self.become_organizer(user, "test")

        # Simulate a GET request to the /my-events endpoint
        response = self.client.get('/api/events/my-events', headers={'Authorization': f'Bearer {token}'})

        # Check that the response status code is 400
        self.assertEqual(response.status_code, 400)

        # Check that the response contains the correct error message
        self.assertEqual(response.json(), {'error': 'Unexpected error occurred'})

    
    # ## Test list all event function
    def test_valid_list_all_event(self):
        response  = self.client.get('/api/events/events')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

        
        
    def test_get_detail(self):
        response = self.client.get(f'/api/events/{self.event_test.id}')
        self.assertEqual(response.status_code , 200)
        self.assertTrue(len([response.json()]), 1)
        
        
    def test_upload_image_event(self):
        token = self.get_token_for_user(self.test_user)
        image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'some content',
            content_type='image/png'
        )
        
        response = self.client.post(f"/api/events/{self.event_test.id}/upload/event-image/", 
                                    headers={'Authorization': f'Bearer {token}'},
                                    data = {'file': image_file})
        self.assertTrue(response.status_code , 200)
        
        
    def test_invalid_user_upload_image_event(self):
        user = self.create_user("test","test")
        
        token = self.get_token_for_user(user)
        
        image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'some content',
            content_type='image/png'
        )
        response = self.client.post(f"/api/events/{self.event_test.id}/upload/event-image/", 
                                    headers={'Authorization': f'Bearer {token}'},
                                    data = {'file': image_file})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'User is not an organizer')
        
        
    def test_invalid_organizer_upload_image_event(self):
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        organizer=  self.become_organizer(user ,"test")
        
        image_file = self.create_test_image()
        response = self.client.post(f"/api/events/{self.event_test.id}/upload/event-image/", 
                                    headers={'Authorization': f'Bearer {token}'},
                                    data = {'file': image_file})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'You are not allowed to upload an image for this event.')
        
    def test_invalid_image_format(self):
        token = self.get_token_for_user(self.test_user)
        
        image_file = SimpleUploadedFile(
            name='test_image.gif',
            content=b'some content',
            content_type='image/gif'
        )
        
        response = self.client.post(f"/api/events/{self.event_test.id}/upload/event-image/", 
                                    headers={'Authorization': f'Bearer {token}'},
                                    data = {'file': image_file})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid file type. Only JPEG and PNG are allowed.' )
        
    def test_invalid_exceed_size_image(self):
        EXCEED_SIZE = 10 * 1024 * 1024
        token = self.get_token_for_user(self.test_user)
        
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'some content' * EXCEED_SIZE,
            content_type='image/jpg'
        )
        
        response = self.client.post(f"/api/events/{self.event_test.id}/upload/event-image/", 
                                    headers={'Authorization': f'Bearer {token}'},
                                    data = {'file': image_file})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'File size exceeds the limit of 10.0 MB.')
        
    def test_set_image_url_event(self):
        token = self.get_token_for_user(self.test_user)
        image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'some content',
            content_type='image/png'
        )
        
        
        response = self.client.post(f"/api/events/{self.event_test.id}/upload/event-image/", 
                                    headers={'Authorization': f'Bearer {token}'},
                                    data = {'file': image_file})
        
        self.assertEqual(response.status_code, 200)
        
        
    @patch("boto3.client")
    def test_upload_event_image_s3_client_error(self, mock_boto_client):
        # Set up a mock S3 client and simulate ClientError on delete_object and upload_fileobj
        mock_s3_client = MagicMock()
        mock_s3_client.delete_object.side_effect = ClientError(
            {"Error": {"Code": "NoSuchKey", "Message": "The specified key does not exist."}},
            "DeleteObject"
        )
        mock_s3_client.upload_fileobj.side_effect = ClientError(
            {"Error": {"Code": "InternalError", "Message": "Internal error"}},
            "UploadFileObject"
        )
        mock_boto_client.return_value = mock_s3_client

        # Set up a mock image file
        image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'some content',
            content_type='image/png'
        )

        # Call the view that handles the S3 object deletion and upload
        token = self.get_token_for_user(self.test_user)
        response = self.client.post(f"/api/events/{self.event_test.id}/upload/event-image/", 
                                    headers={'Authorization': f'Bearer {token}'},
                                    data = {'file': image_file})
        
        # Assert that the response has a 400 status code and contains the expected error messages
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'S3 upload failed: An error occurred (InternalError) when calling the UploadFileObject operation: Internal error')

        # Assert that the delete_object and upload_fileobj methods were called as expected
        
    @patch("boto3.client")
    def test_upload_image_caught_exception(self, mock_boto_client):
        mock_boto_client.side_effect = Exception("Some unexpected error")

        # Make a request
        image_file = self.create_test_image()
        token = self.get_token_for_user(self.test_user)

        # Call the API endpoint
        response = self.client.post(
            f"/api/events/{self.event_test.id}/upload/event-image/",
            data={'file': image_file},
            headers={'Authorization': f'Bearer {token}'},
        )
        # Assert that the error message is in the response
        self.assertEqual(response.status_code, 400)
        self.assertIn("Upload failed", response.json()["error"])
        
        
    def test_get_comment(self):
        response = self.client.get(f"/api/events/{self.event_test.id}/comments")
        self.assertEqual(response.status_code , 200)
        self.assertEqual(response.json(),[])
        
        
    def test_edit_event(self):
        token = self.get_token_for_user(self.test_user)
        data = { 
            "event_name": "Test edit"
        }
        response = self.client.patch(f'/api/events/{self.event_test.id}/edit', data = json.dumps(data),headers={'Authorization': f'Bearer {token}'})
    
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.json()['event_name'], "Test edit")
        
        
    def test_invalid_organizer_edit(self):
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        organizer = self.become_organizer(user, "test")
        data = {
            "category": "CONFERENCE",
            "dress_code": "CASUAL",
            "event_name": "Test edit",
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
        response = self.client.patch(f"/api/events/{self.event_test.id}/edit", headers={'Authorization': f'Bearer {token}'}, data  = json.dumps(data) )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['error'],'You are not allowed to edit this event.')
        
        
    def test_edit_not_exist_event(self):
        token = self.get_token_for_user(self.test_user)
        data = {
            "category": "CONFERENCE",
            "dress_code": "CASUAL",
            "event_name": "Test edit",
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
        
        response = self.client.patch(f"/api/events/{10000}/edit", headers={'Authorization': f'Bearer {token}'}, data = json.dumps(data))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'Event not found')
        
    def test_organizer_does_not_exist(self):
        user = self.create_user("test", "Test")
        token = self.get_token_for_user(user)
        data = {
            "category": "CONFERENCE",
            "dress_code": "CASUAL",
            "event_name": "Test edit",
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
        
        response = self.client.patch(f"/api/events/{self.event_test.id}/edit", headers={'Authorization': f'Bearer {token}'}, data  = json.dumps(data))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'User is not an organizer')
        
    
    @patch('api.models.Event.objects.get')
    def test_edit_caught_exception(self, mock_event_get):
        mock_event_get.side_effect = Exception("Some unexpected error")
        token = self.get_token_for_user(self.test_user)
        
        data = {
            "category": "CONFERENCE",
            "dress_code": "CASUAL",
            "event_name": "Test edit",
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

        response = self.client.patch(
            f"/api/events/{self.event_test.id}/edit",
            headers={'Authorization': f'Bearer {token}'},
            data= json.dumps(data)
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Some unexpected error", response.json().get("error"))
        

        
    def test_available_spot(self):
        event = Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user"),
            start_date_event=timezone.now(),
            end_date_event= timezone.now() + datetime.timedelta(days = 1),  # Ensure it ends after it starts
            start_date_register=timezone.now() - datetime.timedelta(days = 2),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 3),  # Registration ends when the event starts
            max_attendee= 100,
            description=fake.text(max_nb_chars=200),
            event_image = fake.file_name()
        )
        self.assertEqual(event.available_spot() , 100)
        
        
    def test_public_event_no_domain_restrictions(self):
        email = "user@anydomain.com"
        self.assertTrue(self.public_event.is_email_allowed(email))

    def test_private_event_no_domain_restrictions(self):
        self.private_event.allowed_email_domains = ""
        email = "user@anydomain.com"
        self.assertTrue(self.private_event.is_email_allowed(email))

    def test_private_event_with_allowed_domain(self):
        email = "user@example.com"
        self.assertTrue(self.private_event.is_email_allowed(email))

    def test_private_event_with_disallowed_domain(self):
        email = "user@notallowed.com"
        self.assertFalse(self.private_event.is_email_allowed(email))

    def test_invalid_email_format(self):
        email = "invalid-email-format"
        self.assertFalse(self.private_event.is_email_allowed(email))
        
        
    def test_private_event_with_invalid_email_domains(self):
        # Create an event with invalid email domains for a private event
        event = Event(
            event_name="Private Event",
            organizer=self.organizer,
            start_date_event=timezone.now() + datetime.timedelta(days=10),
            end_date_event=timezone.now() + datetime.timedelta(days=11),
            start_date_register=timezone.now(),
            end_date_register=timezone.now() + datetime.timedelta(days=9),
            visibility="PRIVATE",
            allowed_email_domains="example..com, valid.com"
        )

        # Attempt to clean and expect a ValidationError due to invalid domain format
        with self.assertRaises(ValidationError) as cm:
            event.clean()
        
        # Check if the error message contains "Invalid domain(s)"
        self.assertIn("Invalid domain(s)", str(cm.exception))
        
    def test_event_with_start_date_after_end_date(self):
        # Create an event where the start date is after the end date
        event = Event(
            event_name="Invalid Date Event",
            organizer=self.organizer,
            start_date_event=timezone.now() + datetime.timedelta(days=10),
            end_date_event=timezone.now() + datetime.timedelta(days=9),  # End date is before start date
            start_date_register=timezone.now(),
            end_date_register=timezone.now() + datetime.timedelta(days=5),
            visibility="PUBLIC"
        )

        # Attempt to clean and expect a ValidationError due to invalid date order
        with self.assertRaises(ValidationError) as cm:
            event.clean()
        
        # Check if the error message is "End date must be after start date."
        self.assertIn("End date must be after start date.", str(cm.exception))
    
        
        
        

   
        
        
        
        
        
        
        
        

        
        

        
        

        

        
        
        

        
        
        

    


