from .utils.utils_event import EventModelsTest, timezone,datetime, Event


class EventTest(EventModelsTest):
    
    def test_create_event(self):
        # Prepare event data without wrapping it in 'data'
        event_data = {
            'event_name': 'Annual Tech Conference',
            'start_date_event': timezone.now() + datetime.timedelta(days=1),  # Start tomorrow
            'end_date_event': timezone.now() + datetime.timedelta(days=2),    # End the day after
            'start_date_register': timezone.now(),                    # Registration starts now
            'end_date_register': timezone.now() + datetime.timedelta(days=5), # Registration ends in 5 days
            'description': 'A tech event for showcasing new innovations.',
            'max_attendee': 100
        }

        # Send the event data directly
        response = self.client.post(self.event_create_url, json=event_data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Event.objects.filter(event_name = "Annual Tech Conference").exists())
        print(response.json())
        

        
        
        

    


