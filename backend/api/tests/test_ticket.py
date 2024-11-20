from .utils.utils_ticket import TicketModelsTest, Organizer, Event, Ticket, fake, timezone,datetime,AttendeeUser,patch, ValidationError
import logging
logging.disable(logging.CRITICAL)

class TicketTestAPI(TicketModelsTest):
    
    def test_only_attendeeUser_can_see_my_event(self):
        normal_user = self.create_user("test","test")
        token  = self.get_token_for_user(normal_user)
        response = self.client.get(self.user_list_event_url+ str(normal_user.id),  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        
    def test_invalid_list_event(self):
        normal_user = self.create_user("test","test")
        token  = self.get_token_for_user(normal_user)
        response = self.client.get(self.user_list_event_url+ str(1000000),  headers={'Authorization': f'Bearer {token}'})
        self.assertTrue(response.status_code , 404)
        self.assertEqual(response.json()['error'], 'User not found')
        
        
    def test_user_register_same_event(self):
        user=  self.create_user("test","test")
        token = self.get_token_for_user(user)
        ticket = Ticket.objects.create(attendee= user , event=  self.event_test)    
        response = self.client.post(self.user_reserve_event_url + str(self.event_test.id) + '/register',  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'User has already registered for this event.')
        
        
        
    def test_organizer_can_list_event(self):
        normal_user = self.create_user("test","test")
        organizer = self.become_organizer(normal_user, "test")
        token = self.get_token_for_user(organizer)
        response = self.client.get(self.user_list_event_url+ str(organizer.id),  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        
    def test_user_register_event(self):
        normal_user = self.create_user('test','test')
        token = self.get_token_for_user(normal_user)
        response = self.client.post(self.user_reserve_event_url + str(self.event_test.id) + '/register',  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Ticket.objects.filter(event = self.event_test).exists())
        
    def test_organizer_register_event(self):
        normal_user = self.create_user('test','test')
        organizer = self.become_organizer(normal_user,'test_organizer')
        token = self.get_token_for_user(normal_user)
        response = self.client.post(self.user_reserve_event_url + str(self.event_test.id) + '/register',  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)
        
    def test_organizer_cannot_register_own_event(self):
        token = self.get_token_for_user(self.test_user)
        response = self.client.post(self.user_reserve_event_url + str(self.event_test.id) + '/register',  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Organizer cannot register for their own event.', response.json().get("error", ""))
                
    def test_user_cannot_register_full_event(self):
        event_test = Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user"),
            start_date_register=timezone.now() - datetime.timedelta(days = 2),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 1),  # Registration ends when the event starts
            start_date_event=timezone.now(),
            end_date_event= timezone.now() + datetime.timedelta(days = 1),  # Ensure it ends after it starts
            max_attendee=1,
            description=fake.text(max_nb_chars=200)
        )
        normal_user = self.create_user("test","test")
        token = self.get_token_for_user(normal_user)
        Ticket.objects.create(attendee= self.test_user, event=  event_test)
        response = self.client.post(self.user_reserve_event_url + str(event_test.id) + '/register',  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('This event has reached the maximum number of attendees', response.json().get("error", ""))

        
        
    def test_user_not_falls_in_register_dates(self):
        normal_user = self.create_user("test","test")
        token = self.get_token_for_user(normal_user)
        event_test = Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user"),
            start_date_register=timezone.now() + datetime.timedelta(days = 2),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 1),  # Registration ends when the event starts
            start_date_event=timezone.now(),
            end_date_event= timezone.now() + datetime.timedelta(days = 1),  # Ensure it ends after it starts
            max_attendee=100,
            description=fake.text(max_nb_chars=200)
        )
        response = self.client.post(self.user_reserve_event_url + str(event_test.id) + '/register',  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Registration for this event is not allowed.')
        
        
    def test_user_invalid_age_to_register(self):
        test_user = AttendeeUser.objects.create_user(
            username='attendeeuser1234',
            password='password123',
            first_name='Jane',
            last_name='Doe',
            birth_date='2024-11-08',
            phone_number='9876543210',
            email='jane12334.doe@example.com'
        )
        event_test = Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user"),
            start_date_register=timezone.now(),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 1),  # Registration ends when the event starts
            start_date_event=timezone.now()+ datetime.timedelta(days = 2),
            end_date_event= timezone.now() + datetime.timedelta(days = 3),  # Ensure it ends after it starts
            max_attendee=100,
            description=fake.text(max_nb_chars=200),
            min_age_requirement = 20
        )
        token = self.get_token_for_user(test_user)
        response = self.client.post(self.user_reserve_event_url + str(event_test.id) + '/register',  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'You must be at least 20 years old to attend this event.')
        
    def test_none_birth_date_register(self):
        test_user = AttendeeUser.objects.create_user(
            username='attendeeuser1234',
            password='password123',
            first_name='Jane',
            last_name='Doe',
            birth_date= None,
            phone_number='9876543210',
            email='jane12334.doe@example.com'
        )
        event_test = Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user"),
            start_date_register=timezone.now(),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 1),  # Registration ends when the event starts
            start_date_event=timezone.now()+ datetime.timedelta(days = 2),
            end_date_event= timezone.now() + datetime.timedelta(days = 3),  # Ensure it ends after it starts
            max_attendee=100,
            description=fake.text(max_nb_chars=200),
            min_age_requirement = 20
        )
        token = self.get_token_for_user(test_user)
        response = self.client.post(self.user_reserve_event_url + str(event_test.id) + '/register',  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Please set your birth date in account information.")
        
    def test_invalid_registeration_status(self):
        event_test = Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user"),
            start_date_register=timezone.now(),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 1),  # Registration ends when the event starts
            start_date_event=timezone.now()+ datetime.timedelta(days = 2),
            end_date_event= timezone.now() + datetime.timedelta(days = 3),  # Ensure it ends after it starts
            max_attendee=100,
            description=fake.text(max_nb_chars=200),
            status_registeration = "CLOSED",
        )
        token = self.get_token_for_user(self.test_user)
        response = self.client.post(self.user_reserve_event_url + str(event_test.id) + '/register',  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], f'Registration for this event is {event_test.status_registeration.lower()} now.')
        

    def test_invalid_register_private_event(self):
        event_test = Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user"),
            start_date_register=timezone.now(),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 1),  # Registration ends when the event starts
            start_date_event=timezone.now()+ datetime.timedelta(days = 2),
            end_date_event= timezone.now() + datetime.timedelta(days = 3),  # Ensure it ends after it starts
            max_attendee=100,
            description=fake.text(max_nb_chars=200),
            min_age_requirement = 20,
            visibility =  "PRIVATE",
            allowed_email_domains = "ku.th"
        )
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        response = self.client.post(self.user_reserve_event_url + str(event_test.id) + '/register',  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code , 403)
        self.assertEqual(response.json()['error'], 'Your email domain is not authorized to register for this event.' )
        
        
        
    def test_cancel_ticket(self):
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        event_test = Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user"),
            start_date_register=timezone.now(),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 1),  # Registration ends when the event starts
            start_date_event=timezone.now()+ datetime.timedelta(days = 2),
            end_date_event= timezone.now() + datetime.timedelta(days = 3),  # Ensure it ends after it starts
            max_attendee=100,
            description=fake.text(max_nb_chars=200),
        )
        ticket = Ticket.objects.create(event = event_test, attendee = user)
        response = self.client.delete(f"/api/tickets/{ticket.id}/cancel" , headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code , 200)
        self.assertEqual(response.json()['success'], f"Ticket with ID {ticket.id} has been canceled.")
        self.assertFalse(Ticket.objects.filter(event = event_test, attendee = user).exists())
        
        
    def test_invalid_cancel_ticket(self):
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        event_test = Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user"),
            start_date_register=timezone.now(),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 1),  # Registration ends when the event starts
            start_date_event=timezone.now()+ datetime.timedelta(days = 2),
            end_date_event= timezone.now() + datetime.timedelta(days = 3),  # Ensure it ends after it starts
            max_attendee=100,
            description=fake.text(max_nb_chars=200),
            min_age_requirement = 20
        )
        ticket = Ticket.objects.create(event = event_test, attendee = user)
        response = self.client.delete(f'/api/tickets/{100}/cancel',  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'],  'Ticket with ID 100 does not exist or you do not have permission to cancel it.')
        
        
    def test_get_ticket_detail(self):
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        event_test = Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user"),
            start_date_register=timezone.now(),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 1),  # Registration ends when the event starts
            start_date_event=timezone.now()+ datetime.timedelta(days = 2),
            end_date_event= timezone.now() + datetime.timedelta(days = 3),  # Ensure it ends after it starts
            max_attendee=100,
            description=fake.text(max_nb_chars=200),
            min_age_requirement = 20
        )
        ticket = Ticket.objects.create(event = event_test, attendee = user)
        response = self.client.get(f"/api/tickets/{ticket.id}",  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], ticket.id)
        
    
    def test_invalid_get_ticket_detail(self):
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        response = self.client.get(f"/api/tickets/{100}",  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "Ticket not found")
        
        
    @patch("api.views.strategy.ticket_strategy.get_object_or_404")
    def test_internal_server_error(self, mock_get_object_or_404):
        
        mock_get_object_or_404.side_effect = Exception("Simulated server error")
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        event_test = Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user"),
            start_date_register=timezone.now(),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 1),  # Registration ends when the event starts
            start_date_event=timezone.now()+ datetime.timedelta(days = 2),
            end_date_event= timezone.now() + datetime.timedelta(days = 3),  # Ensure it ends after it starts
            max_attendee=100,
            description=fake.text(max_nb_chars=200),
            min_age_requirement = 20
        )
        ticket = Ticket.objects.create(event = event_test, attendee = user)
        try:
            response = self.client.get(f"/api/tickets/{ticket.id}",  headers={'Authorization': f'Bearer {token}'})
        except Exception as e:
            self.fail(f"Unexpected exception occurred: {str(e)}")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['error'], 'Internal server error')
        
        
    @patch("api.models.Ticket.save")
    def test_register_for_event_general_exception(self, mock_save):
        # Mock Ticket.save to raise a general Exception
        mock_save.side_effect = Exception("Unexpected error")
        user = self.create_user("test","test")
    
        token = self.get_token_for_user(user)
        response = self.client.post(self.user_reserve_event_url + str(self.event_test.id) + '/register',  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['error'], "Internal server error")
        
        
    @patch("api.utils.TicketNotificationManager.send_cancellation_notification")
    def test_cancel_ticket_email_exception(self, mock_send_notification):
        # Simulate an error when sending the cancellation email
        mock_send_notification.side_effect = Exception("Email sending failed")
        ticket = Ticket.objects.create(event = self.event_test, attendee =self.test_user)
        token = self.get_token_for_user(self.test_user)

        # Call the delete endpoint for canceling the ticket
        response = self.client.delete(f'/api/tickets/{ticket.id}/cancel',  headers={'Authorization': f'Bearer {token}'})
        # Assert the response status code is 500 as per the updated logic
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['error'], 'Failed to send cancellation email')
        
        
        
    def test_ticket_number_generation_on_save(self):
        # Create a ticket without a ticket number and save it
        ticket = Ticket(event=self.event_test, attendee=self.test_user)
        ticket.save()
        # Ensure the ticket number was generated and is unique
        self.assertTrue(ticket.ticket_number)
        self.assertEqual(Ticket.objects.filter(ticket_number=ticket.ticket_number).count(), 1)
        
            
    def test_cancellation_date_not_changed_if_already_set(self):
        # Create a ticket with a pre-set cancellation date and save it
        cancellation_date = timezone.now() - timezone.timedelta(days=1)
        ticket = Ticket(event=self.event_test, attendee=self.test_user, status='CANCELLED', cancellation_date=cancellation_date)
        ticket.save()
        
        # Ensure the pre-set cancellation date remains unchanged
        self.assertEqual(ticket.cancellation_date, cancellation_date)
        
    def test_sent_reminder(self):
        ticket = Ticket.objects.create(event = self.event_test, attendee =self.test_user)
        response = self.client.post(f'/api/tickets/{ticket.id}/send-reminder',  headers={'Authorization': f'Bearer {self.get_token_for_user(self.test_user)}'})
        self.assertEqual(response.status_code, 200)
        
    @patch("api.models.Ticket.objects.get")
    def test_cancel_ticket_general_exception(self, mock_get):

        mock_get.side_effect = Exception("Database error")
        ticket = Ticket.objects.create(event = self.event_test, attendee =self.test_user)
        token = self.get_token_for_user(self.test_user)

        response = self.client.delete(f"/api/tickets/{ticket.id}/cancel",  headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['error'], 'Internal server error')
        
        
    def test_cannot_cancel_already_cancelled_ticket(self):
        # Cancel the ticket once
        ticket = Ticket.objects.create(attendee = self.test_user, event = self.event_test, )
        ticket.cancel_ticket(reason="No longer attending")

        # Try cancelling it again, which should raise a ValidationError
        with self.assertRaises(ValidationError) as e:
            ticket.cancel_ticket(reason="Attempted second cancellation")
        
        # Check that the correct error message is in the exception
        self.assertIn("Ticket is already cancelled.", str(e.exception))
        
    
   

        
        
        
        
        
    

        
        
        
        
        
        
        
        
    
        