from .utils.utils_organizer import OrganizerModelsTest, Organizer, Event,fake
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
        
    def test_valid_update_organizer(self):
        normal_user = self.create_user("test1", "test1")
        organizer = self.become_organizer(normal_user, "Test")
        token = self.get_token_for_user(normal_user)
        new_data = {
            "id":organizer.id,
            "organizer_name": fake.name(),
            "email": fake.email(),
            }
        response = self.client.put(self.update_organizer_url, json = new_data ,headers={'Authorization': f'Bearer {token}'} )
        self.assertEqual(response.status_code, 200)
        
    def test_create_new_organizer_but_already_taken_name(self):
        normal_user = self.create_user("test1","test1")
        organizer = self.become_organizer(normal_user, "test")
        normal_user1= self.create_user("Test2","test2")
        token = self.get_token_for_user(normal_user1)
        data = {
            "organizer_name": "test",
            "email": fake.email(),
        }
        response  = self.client.post(self.apply_organizer_url, data = data, headers={'Authorization': f'Bearer {token}'})
        self.assertTrue(response.status_code, 400)
        self.assertTrue(Organizer.objects.filter(organizer_name = "test").count(), 1)
        
        
        
    def test_update_organizer_but_already_taken_name(self):
        normal_user = self.create_user("test1","test1")
        organizer = self.become_organizer(normal_user,"test")
        normal_user1 = self.create_user("test2","test2")
        token = self.get_token_for_user(normal_user1)
        organizer1 = self.become_organizer(normal_user1,"test1")
        
        new_data = {
            "organizer_name": "test",
            "email": fake.email(),
            }
        response = self.client.put(self.update_organizer_url, json = new_data ,headers={'Authorization': f'Bearer {token}'} )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Organizer.objects.filter(organizer_name = "test").count(), 1)
        self.assertIn('Organizer name is already taken', response.json().get("error", ""))
    
    def test_valid_revoke_organizer(self):
        normal_user = self.create_user("test1","test1")
        organizer= self.become_organizer(normal_user, "test1")
        token = self.get_token_for_user(normal_user)
        response = self.client.delete(self.revoke_organizer_url,headers={'Authorization': f'Bearer {token}'} )
        self.assertEqual(response.status_code, 204)
        self.assertIn(f'Organizer role revoked for user {normal_user.id}.', response.json().get("success", ""))
        
    def test_invalid_revok_organizer(self):
        normal_user = self.create_user("test1","test1")
        token = self.get_token_for_user(normal_user)
        response = self.client.delete(self.revoke_organizer_url,headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 404)
        
    def test_valid_view_organizer(self):
        normal_user =self.create_user("test1","test1")
        token = self.get_token_for_user(normal_user)
        organizer = self.become_organizer(normal_user, "test")
        response = self.client.get(self.view_organizer_url, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        
    def test_invalid_view_organizer(self):
        normal_user = self.create_user("test","test")
        token = self.get_token_for_user(normal_user)
        response = self.client.get(self.view_organizer_url, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('User is not an organizer', response.json().get("error", ""))
        
        
        
        
        
        
    
    
        