from .utils.utils_event import EventModelsTest, timezone,datetime, Event, Organizer, fake, patch


class EventTest(EventModelsTest):
    
    def test_organizer_create_event(self):
        # Prepare event data without wrapping it in 'data'
        user = self.create_user("become_organizer", "become_organizer")
        token = self.get_token_for_user(user)
        organizer = self.become_organizer(user, "become_organizer")
        event_data = {
            'event_name': 'Annual Tech Conference',
            'start_date_event': timezone.now() + datetime.timedelta(days=2),  # Start tomorrow
            'end_date_event': timezone.now() + datetime.timedelta(days=3),    # End the day after
            'start_date_register': timezone.now(),                    # Registration starts now
            'end_date_register': timezone.now() + datetime.timedelta(days=1), # Registration ends in 5 days
            'description': 'A tech event for showcasing new innovations.',
            'max_attendee': 100
        }

        # Send the event data directly
        response = self.client.post(self.event_create_url, json=event_data, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Event.objects.filter(event_name = "Annual Tech Conference").exists())

        
    def test_user_cannot_create_event(self):
        just_user = self.create_user("not_organizer", "not_organizer")
        token  = self.get_token_for_user(just_user)
        event_data = {
            'event_name': 'Annual Tech Conference',
            'start_date_event': timezone.now() + datetime.timedelta(days=1),  # Start tomorrow
            'end_date_event': timezone.now() + datetime.timedelta(days=2),    # End the day after
            'start_date_register': timezone.now(),                    # Registration starts now
            'end_date_register': timezone.now() + datetime.timedelta(days=5), # Registration ends in 5 days
            'description': 'A tech event for showcasing new innovations.',
            'max_attendee': 100
        }
        
        self.assertFalse(Organizer.objects.filter(user = just_user).exists())
        response = self.client.post(
            self.event_create_url,
            json=event_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], "You are not an organizer.")
        
    
    def test_can_register(self):
        event_test = Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user"),
            start_date_register=timezone.now() - datetime.timedelta(days = 2),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 1),  # Registration ends when the event starts
            start_date_event=timezone.now() + datetime.timedelta(days = 3),
            end_date_event= timezone.now() + datetime.timedelta(days = 4),  # Ensure it ends after it starts
            max_attendee=fake.random_int(min=10, max=500),
            description=fake.text(max_nb_chars=200)
        )
        self.assertTrue(event_test.can_register())
        
    def test_date_input_is_valid(self):
        event_data = {
            'event_name': 'Annual Tech Conference',
            'start_date_register': timezone.now(),                    # Registration starts now
            'end_date_register': timezone.now() + datetime.timedelta(days=1), # Registration ends in 5 days
            'start_date_event': timezone.now() + datetime.timedelta(days=2),  # Start tomorrow
            'end_date_event': timezone.now() + datetime.timedelta(days=3),    # End the day after
            'description': 'A tech event for showcasing new innovations.',
            'max_attendee': 100
        }
        normal_user = self.create_user("test", "test")
        organizer = self.become_organizer(normal_user, "test")
        token  = self.get_token_for_user(normal_user)
        response = self.client.post(self.event_create_url, json=event_data, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        
    def test_date_input_invalid(self):
        event_data = {
            'event_name': 'Annual Tech Conference',
            'start_date_register': timezone.now(),                    # Registration starts now
            'end_date_register': timezone.now() - datetime.timedelta(days=2), # Registration ends in 5 days
            'start_date_event': timezone.now() + datetime.timedelta(days=2),  # Start tomorrow
            'end_date_event': timezone.now() + datetime.timedelta(days=3),    # End the day after
            'description': 'A tech event for showcasing new innovations.',
            'max_attendee': 100
        }
        normal_user = self.create_user("test", "test")
        organizer = self.become_organizer(normal_user, "test")
        token  = self.get_token_for_user(normal_user)
        response = self.client.post(self.event_create_url, json=event_data, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter valid date', response.json().get("error", ""))
        
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
        
    def test_valid_get_all_events(self):
        response = self.client.get(self.list_event_url)
        self.assertEqual(response.status_code, 200)
        
    def test_valid_get_event_detail(self):
        response = self.client.get(self.get_event_detail_url + str(self.event_test.id))
        self.assertEqual(response.status_code, 200)
        
        
    def test_valid_edit_event(self):
        new_data = {
            "event_name": fake.company(),
            "start_date_register": timezone.now() - datetime.timedelta(days = 2),
            "end_date_register": timezone.now() - datetime.timedelta(days = 1),
            "start_date_event": timezone.now(),
            "end_date_event": timezone.now() + datetime.timedelta(days = 1),
            "max_attendee": 1,
            "description": fake.text(max_nb_chars=200)
        }
        token = self.get_token_for_user(self.test_user)
        
        response = self.client.put(self.edit_event_url + str(self.event_test.id), json = new_data ,headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 204)
        
        
    def test_invalid_organizer_edit_event(self):
        new_data = {
            "event_name": fake.company(),
            "start_date_register": timezone.now() - datetime.timedelta(days = 2),
            "end_date_register": timezone.now() - datetime.timedelta(days = 1),
            "start_date_event": timezone.now(),
            "end_date_event": timezone.now() + datetime.timedelta(days = 1),
            "max_attendee": 1,
            "description": fake.text(max_nb_chars=200)
        }
        normal_user = self.create_user("test","test")
        token = self.get_token_for_user(normal_user)
        response = self.client.put(self.edit_event_url + str(self.event_test.id), json = new_data ,headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 404)
        normal_user1  = self.create_user("test1","test1")
        organizer = self.become_organizer(normal_user1, "test_organizer")
        token1 = self.get_token_for_user(normal_user1)
        response = self.client.put(self.edit_event_url + str(self.event_test.id), json = new_data ,headers={'Authorization': f'Bearer {token1}'})
        self.assertIn('You are not allowed to edit this event.', response.json().get("error", ""))
        self.assertTrue(response.status_code, 403)
        
        
    def test_edit_does_not_exist(self):
        normal_user = self.create_user("test","test")
        token = self.get_token_for_user(normal_user)
        new_data = {
            "event_name": fake.company(),
            "start_date_register": timezone.now() - datetime.timedelta(days = 2),
            "end_date_register": timezone.now() - datetime.timedelta(days = 1),
            "start_date_event": timezone.now(),
            "end_date_event": timezone.now() + datetime.timedelta(days = 1),
            "max_attendee": 1,
            "description": fake.text(max_nb_chars=200)
        }
        response = self.client.put(self.edit_event_url + str(2), json = new_data ,headers={'Authorization': f'Bearer {token}'})
        self.assertTrue(response.status_code, 404)
        self.assertIn('Event not found', response.json().get("error", ""))
        
        
    @patch("api.models.Organizer.objects.get")
    def test_get_my_events_unexpected_exception(self, mock_get_organizer):
        # Mock Organizer.objects.get to raise an unexpected exception
        mock_get_organizer.side_effect = Exception(f"Error while retrieving events for organizer {self.test_user.id}")
        token = self.get_token_for_user(self.test_user)

        # Make the request with a JWT token in the header
        response = self.client.get(
            self.organizer_get_events,  # Replace with the actual URL name for your endpoint
            headers={'Authorization': f'Bearer {token}'}
        )
  
        # Assert that the response status is 400 (Bad Request)
        self.assertEqual(response.status_code,  400)

        # Assert that the response contains the error message
        self.assertEqual(response.data['error'], f"Error while retrieving events for organizer {self.test_user.id}")
        
    @patch("api.models.Event.objects.filter")
    def test_list_event_unexpected_exception(self,mock_filter):
            # Simulate a DatabaseError
        mock_filter.side_effect = Exception(f"Error while retrieving events for the homepage")

        response = self.client.get(self.list_event_url)
        self.assertEqual(response.status_code,400)
        self.assertIn(f"Error while retrieving events for the homepage", response.json().get("error", ""))
        
    @patch("api.models.Event.objects.get")
    def test_edit_evnt_unexpected_exception(self, mock_get_event):
        new_data = {
            "event_name": fake.company(),
            "start_date_register": timezone.now() - datetime.timedelta(days = 2),
            "end_date_register": timezone.now() - datetime.timedelta(days = 1),
            "start_date_event": timezone.now(),
            "end_date_event": timezone.now() + datetime.timedelta(days = 1),
            "max_attendee": 1,
            "description": fake.text(max_nb_chars=200)
        }
        mock_get_event.side_effect = Exception(f"Error while editing event {self.event_test.id}")
        token = self.get_token_for_user(self.test_user)
        
        response = self.client.put(self.edit_event_url + str(2), json = new_data ,headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code,400)
        self.assertIn(f"Error while editing event {self.event_test.id}", response.json().get("error", ""))
        

        
        
        
        
        

        
        
        
        
        
        
        
        

        
        

        
        

        

        
        
        

        
        
        

    


