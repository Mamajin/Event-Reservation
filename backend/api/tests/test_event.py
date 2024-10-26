from .utils.utils_event import EventModelsTest, timezone,datetime, Event, Organizer, fake


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
            start_date_event=timezone.now(),
            end_date_event= timezone.now() + datetime.timedelta(days = 1),  # Ensure it ends after it starts
            start_date_register=timezone.now() - datetime.timedelta(days = 2),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 3),  # Registration ends when the event starts
            max_attendee=fake.random_int(min=10, max=500),
            description=fake.text(max_nb_chars=200)
        )
        self.assertTrue(event_test.can_register(), True)
        

        
        

        
        

        

        
        
        

        
        
        

    


