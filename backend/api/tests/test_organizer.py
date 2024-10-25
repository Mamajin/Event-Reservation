from .utils.utils_organizer import OrganizerModelsTest, Organizer, Event
import logging
logging.disable(logging.CRITICAL)

class OrganizerTestAPI(OrganizerModelsTest):
    
    def test_apply_organizer(self):
        normal_user = self.create_user("normal_user", "normal_user")
        token = self.get_token_for_user(normal_user)
        data = {
            "organizer_name": "test_organizer",
            "email": "test@example.com"
        }
        response  = self.client.post(self.apply_organizer_url, data = data, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Organizer.objects.filter(organizer_name = response.json()["organizer_name"]).exists())
        
    def test_user_is_already_an_organizer(self):
        token = self.get_token_for_user(self.test_user)
        data = {
            "organizer_name": "test_organizer",
            "email": "test@example.com"
        }
        response = self.client.post(self.apply_organizer_url,data = data , headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 400)
        self.assertTrue(Organizer.objects.filter(user = self.test_user).exists())
        
        
    def test_only_organizer_delete_own_event(self):
        token = self.get_token_for_user(self.test_user)
        event_id = self.event_test.id
        response  = self.client.delete(self.delete_event_url+str(event_id), headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Event.objects.filter(id = event_id).exists())
        
        
    def test_normal_user_cannot_delete_event(self):
        normal_user = self.create_user("test","test")
        token = self.get_token_for_user(normal_user)
        event_id = self.event_test.id
        response  = self.client.delete(self.delete_event_url+str(event_id), headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 403)
        self.assertIn("User is not an organizer", response.json().get("error", ""))
        
        
    def test_organizer_not_delele_own_event(self):
        normal_user = self.create_user("test1", "test1")
        token = self.get_token_for_user(normal_user)
        organizer_test = self.become_organizer(normal_user,"test_win")
        event_id = self.event_test.id
        response  = self.client.delete(self.delete_event_url+str(event_id), headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Event does not exist or you do not have permission to delete it', response.json().get("error", ""))
        