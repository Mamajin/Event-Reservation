from .utils.utils_ticket import TicketModelsTest, Organizer, Event, Ticket
import logging
logging.disable(logging.CRITICAL)

class TicketTestAPI(TicketModelsTest):
    
    def test_only_attendeeUser_can_see_my_event(self):
        normal_user = self.create_user("test","test")
        token  = self.get_token_for_user(normal_user)
        response = self.client.get(self.user_list_event_url+ str(normal_user.id),  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        
        
    def test_organizer_canregister_event(self):
        normal_user = self.create_user("test","test")
        organizer = self.become_organizer(normal_user, "test")
        token = self.get_token_for_user(organizer)
        response = self.client.get(self.user_list_event_url+ str(organizer.id),  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        
    def test_user_register_event(self):
        normal_user = self.create_user('test','test')
        token = self.get_token_for_user(normal_user)
        response = self.client.post(self.user_reserve_event_url+ str(self.event_test.id)+"/reserve",  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Ticket.objects.filter(event = self.event_test).exists())
        
    def test_organizer_register_event(self):
        normal_user = self.create_user('test','test')
        organizer = self.become_organizer(normal_user,'test_organizer')
        token = self.get_token_for_user(normal_user)
        response = self.client.post(self.user_reserve_event_url+ str(self.event_test.id)+"/reserve",  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        

    def test_organizer_cannot_register_own_event(self):
        token = self.get_token_for_user(self.test_user)
        response = self.client.post(self.user_reserve_event_url+ str(self.event_test.id)+"/reserve",  headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 400)
        

        
    def test_user_cancel_event(self):
        normal_user = self.create_user("test","test")
        token = self.get_token_for_user(normal_user)
        ticket = Ticket.objects.create(attendee = normal_user, event = self.event_test)
        response = self.client.delete(self.user_cancel_event_url + str(ticket.id), headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        
    def test_user_can_only_cancel_their_own_registration(self):
        normal_user1 = self.create_user("test","test")
        normal_user2 = self.create_user("test1", "test2")
        token2 = self.get_token_for_user(normal_user2)
        ticket = Ticket.objects.create(attendee = normal_user1, event = self.event_test)
        response = self.client.delete(self.user_cancel_event_url + str(ticket.id), headers={'Authorization': f'Bearer {token2}'})
        self.assertEqual(response.status_code, 400)
        self.assertTrue(Ticket.objects.filter(attendee = normal_user1).exists())
        
        
        
    
        