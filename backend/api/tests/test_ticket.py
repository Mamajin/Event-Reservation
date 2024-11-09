from .utils.utils_ticket import TicketModelsTest, Organizer, Event, Ticket, fake, timezone,datetime,AttendeeUser
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
        

    # def test_user_cancel_event(self):
    #     normal_user = self.create_user("test","test")
    #     token = self.get_token_for_user(normal_user)
    #     ticket = Ticket.objects.create(attendee = normal_user, event = self.event_test)
    #     response = self.client.delete(self.user_cancel_event_url + str(ticket.id), headers={'Authorization': f'Bearer {token}'})
    #     self.assertEqual(response.status_code, 200)
        
    # def test_user_can_only_cancel_their_own_registration(self):
    #     normal_user1 = self.create_user("test","test")
    #     normal_user2 = self.create_user("test1", "test2")
    #     token2 = self.get_token_for_user(normal_user2)
    #     ticket = Ticket.objects.create(attendee = normal_user1, event = self.event_test)
    #     response = self.client.delete(self.user_cancel_event_url + str(ticket.id), headers={'Authorization': f'Bearer {token2}'})
    #     self.assertEqual(response.status_code, 400)
    #     self.assertTrue(Ticket.objects.filter(attendee = normal_user1).exists())
        
        
    def test_user_cannot_register_full_event(self):
        event_test = Event.objects.create(
            event_name=fake.company(),
            organizer= self.become_organizer(self.test_user, "test_user"),
            start_date_register=timezone.now() - datetime.timedelta(days = 2),  # Example for registration start
            end_date_register=timezone.now() + datetime.timedelta(days = 1),  # Registration ends when the event starts
            start_date_event=timezone.now(),
            end_date_event= timezone.now() + datetime.timedelta(days = 1),  # Ensure it ends after it starts
            max_attendee=0,
            description=fake.text(max_nb_chars=200)
        )
        normal_user = self.create_user("test","test")
        token = self.get_token_for_user(normal_user)
        response = self.client.post(self.user_reserve_event_url + str(event_test.id) + '/register',  headers={'Authorization': f'Bearer {token}'})
       
        self.assertEqual(response.status_code, 400)
        self.assertIn('This event has reached the maximum number of attendees', response.json().get("error", ""))
        
    # def test_invalid_list_my_events(self):
    #     normal_user=  self.create_user("test", "test")
    #     token = self.get_token_for_user(normal_user)
    #     response = self.client.get(self.user_list_event_url+str(0),  headers={'Authorization': f'Bearer {token}'})
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json()['error'], "This user does not exists")
        
    # def test_register_with_event_that_does_not_exist(self):
    #     normal_user = self.create_user("test","test")
    #     token = self.get_token_for_user(normal_user)
    #     response = self.client.post(self.user_reserve_event_url+ str(0)+"/reserve",  headers={'Authorization': f'Bearer {token}'})
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(response.json()['error'], "This event does not exists")
    
    # def test_user_register_same_event(self):
    #     normal_user = self.create_user("test","test")
    #     ticket = Ticket.objects.create(event = self.event_test, attendee =normal_user)
    #     token = self.get_token_for_user(normal_user)
    #     response = self.client.post(self.user_reserve_event_url+ str(self.event_test.id)+"/reserve",  headers={'Authorization': f'Bearer {token}'})
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json()['error'], 'You have registered this event already')
        
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
        self.assertEqual(response.json()['error'], 'Registration for this event is not allowed')
        
        
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
        
        
        
        
    

        
        
        
        
        
        
        
        
    
        