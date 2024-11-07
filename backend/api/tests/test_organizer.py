from .utils.utils_organizer import OrganizerModelsTest, Organizer, Event,fake, patch, SimpleUploadedFile, ALLOWED_IMAGE_TYPES
import logging
logging.disable(logging.CRITICAL)

class OrganizerTestAPI(OrganizerModelsTest):
    
    
    def test_apply_organizer(self):
        normal_user = self.create_user("normal_user", "normal_user", "win")
        token = self.get_token_for_user(normal_user)
        data = {
            "organizer_name": "test_organizer",
            "email": "test@example.com",
            "organization_type" : "INDIVIDUAL"
        }
        response  = self.client.post(self.apply_organizer_url, data = data, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Organizer.objects.filter(organizer_name = response.json()["organizer_name"]).exists())
        
    def test_user_is_already_an_organizer(self):
        token = self.get_token_for_user(self.test_user)
        data = {
            "organizer_name": "test_organizer",
            "email": "test@example.com",
            "organization_type" : "INDIVIDUAL"
        }
        response = self.client.post(self.apply_organizer_url,data = data , headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 400)
        self.assertTrue(Organizer.objects.filter(user = self.test_user).exists())
        
    def test_organizer_take_same_name(self):
        user1 = self.create_user("test1",'test1', "win")
        organizer = self.become_organizer(user1, "test_organizer", "win")
        user = self.create_user("test","test", "win1")
        token = self.get_token_for_user(user)

        data = {
            "organizer_name": "test_organizer",
            "email": "tes123@example.com",
            "organization_type" : "INDIVIDUAL"
        }
        response = self.client.post(self.apply_organizer_url,data = data , headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code , 400)
        self.assertEqual(response.json()['error'], 'Organizer name is already taken')
        
    @patch("api.models.Organizer.objects.filter")
    def test_apply_organizer_caught_exception(self, mock_organizer_filter):
        mock_organizer_filter.side_effect = Exception("Some unexpected error")
        user=  self.create_user("win","win","win")
        token = self.get_token_for_user(user)
        data = {
            "organizer_name": "test_organizer",
            "email": "tes123@example.com",
            "organization_type" : "INDIVIDUAL"
        }
        response = self.client.post(self.apply_organizer_url,data = data , headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code , 400)
        self.assertIn('An unexpected error occurred', response.json().get("error"))
        

        
    def test_only_organizer_delete_own_event(self):
        token = self.get_token_for_user(self.test_user)
        event_id = self.event_test.id
        response  = self.client.delete(self.delete_event_url+str(event_id), headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Event.objects.filter(id = event_id).exists())
        
        
    def test_normal_user_cannot_delete_event(self):
        normal_user = self.create_user("test","test", "win")
        token = self.get_token_for_user(normal_user)
        event_id = self.event_test.id
        response  = self.client.delete(self.delete_event_url+str(event_id), headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 403)
        self.assertIn("User is not an organizer", response.json().get("error", ""))
        
        
    def test_organizer_not_delele_own_event(self):
        normal_user = self.create_user("test1", "test1", "win")
        token = self.get_token_for_user(normal_user)
        organizer_test = self.become_organizer(normal_user,"test_win", "test")
        event_id = self.event_test.id
        response  = self.client.delete(self.delete_event_url+str(event_id), headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Event does not exist or you do not have permission to delete it', response.json().get("error", ""))
        
    def test_valid_update_organizer(self):
        user=  self.create_user("test1", "test", "win")
        organizer = self.become_organizer(user, "winwin", "test")
        token = self.get_token_for_user(user)
        data = {
            "organizer_name": "test_organizer1",
            "email": "tes123@example.com",
            "organization_type" : "INDIVIDUAL"
        }
        response = self.client.put(self.update_organizer_url, json = data ,headers={'Authorization': f'Bearer {token}'} )
        
        self.assertEqual(response.status_code, 200)
 
        
    def test_update_organizer_but_already_taken_name(self):
        normal_user = self.create_user("test1","test1", "win")
        organizer = self.become_organizer(normal_user,"test", "test123")
        normal_user1 = self.create_user("test2","test2", "win1")
        token = self.get_token_for_user(normal_user1)
        organizer1 = self.become_organizer(normal_user1,"test1", "test1234")
        
        new_data = {
            "organizer_name": "test",
            "email": fake.email(),
            "organization_type" : "INDIVIDUAL"
            }
        response = self.client.put(self.update_organizer_url, json = new_data ,headers={'Authorization': f'Bearer {token}'} )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Organizer.objects.filter(organizer_name = "test").count(), 1)
        self.assertIn('Organizer name is already taken', response.json().get("error", ""))
    
    def test_valid_revoke_organizer(self):
        normal_user = self.create_user("test1","test1", "win")
        organizer= self.become_organizer(normal_user, "test1", "organizer")
        token = self.get_token_for_user(normal_user)
        response = self.client.delete(self.revoke_organizer_url,headers={'Authorization': f'Bearer {token}'} )
        self.assertEqual(response.status_code, 204)
        self.assertIn(f'Organizer role revoked for user {normal_user.id}.', response.json().get("success", ""))
        
    def test_invalid_revoke_organizer(self):
        normal_user = self.create_user("test1","test1", "win")
        token = self.get_token_for_user(normal_user)
        response = self.client.delete(self.revoke_organizer_url,headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'User is not an organizer')
        
    def test_valid_view_organizer(self):
        normal_user =self.create_user("test1","test1", "win")
        token = self.get_token_for_user(normal_user)
        organizer = self.become_organizer(normal_user, "test", "win")
        response = self.client.get(self.view_organizer_url, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        
    def test_upload_logo(self):
        user = self.create_user("test","test","test")
        organizer = self.become_organizer(user,"test","test")
        token = self.get_token_for_user(user)
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'some content',
            content_type='image/jpg'
        )
        response = self.client.post(f"/{organizer.id}" + self.upload_logo_organizer_url, headers={'Authorization': f'Bearer {token}'}, FILES = {'logo': image_file})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Upload successful')
        
    def test_invalid_type_image(self):
        user = self.create_user("test","test","test")
        organizer = self.become_organizer(user,"test","test")
        token = self.get_token_for_user(user)
        image_file = SimpleUploadedFile(
            name='test_image.gif',
            content=b'some content',
            content_type='image/gif'
        )
        response = self.client.post(f"/{organizer.id}" + self.upload_logo_organizer_url, headers={'Authorization': f'Bearer {token}'}, FILES = {'logo': image_file})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid file type. Only JPEG and PNG are allowed.')
        
    def test_invalid_image_size(self):
        user = self.create_user("test","test","test")
        organizer = self.become_organizer(user,"test","test")
        token = self.get_token_for_user(user)
        image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'some content' * self.EXCEED_SIZE,
            content_type='image/png'
        )
        response = self.client.post(f"/{organizer.id}" + self.upload_logo_organizer_url, headers={'Authorization': f'Bearer {token}'}, FILES = {'logo': image_file})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'File size exceeds the limit of 10.0 MB.')
        
    
        
        
        
        
        
        
        
        
        
    
    
        