from .utils.utils_organizer import OrganizerModelsTest, Organizer, Event,fake, patch, SimpleUploadedFile, ALLOWED_IMAGE_TYPES, Mock, ClientError, MagicMock
import logging
import json
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
        response  = self.client.post('/api/organizers/apply-organizer', data = data, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Organizer.objects.filter(organizer_name = response.json()["organizer_name"]).exists())
        
    def test_user_is_already_an_organizer(self):
        token = self.get_token_for_user(self.test_user)
        data = {
            "organizer_name": "test_organizer",
            "email": "test@example.com",
            "organization_type" : "INDIVIDUAL"
        }
        response = self.client.post('/api/organizers/apply-organizer', data = data , headers={'Authorization': f'Bearer {token}'})
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
        response = self.client.post('/api/organizers/apply-organizer', data = data , headers={'Authorization': f'Bearer {token}'})
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
        response = self.client.post('/api/organizers/apply-organizer', data = data , headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code , 400)
        self.assertIn(response.json()['error'], 'An unexpected error occurred')
        

        
    def test_only_organizer_delete_own_event(self):
        token = self.get_token_for_user(self.test_user)
        event_id = self.event_test.id
        response  = self.client.delete('/api/organizers/delete-event/'+str(event_id), headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Event.objects.filter(id = event_id).exists())
        
        
    def test_normal_user_cannot_delete_event(self):
        normal_user = self.create_user("test","test", "win")
        token = self.get_token_for_user(normal_user)
        event_id = self.event_test.id
        response  = self.client.delete('/api/organizers/delete-event/'+str(event_id), headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 403)
        self.assertIn(response.json()['error'], "User is not an organizer")
        
        
    def test_organizer_not_delele_own_event(self):
        normal_user = self.create_user("test1", "test1", "win")
        token = self.get_token_for_user(normal_user)
        organizer_test = self.become_organizer(normal_user,"test_win", "test")
        event_id = self.event_test.id
        response  = self.client.delete('/api/organizers/delete-event/'+str(event_id), headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 404)
        self.assertIn(response.json().get('error', ''), 'Event does not exist or you do not have permission to delete it')
        
    def test_valid_update_organizer(self):
        user=  self.create_user("test1", "test", "win")
        organizer = self.become_organizer(user, "winwin", "test")
        token = self.get_token_for_user(user)
        data = {
            "organizer_name": "test_organizer1",
            "email": "tes123@example.com",
            "organization_type" : "INDIVIDUAL"
        }
        response = self.client.patch(
            '/api/organizers/update-organizer', 
            data=json.dumps(data),
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
                },
            )
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
        response = self.client.patch('/api/organizers/update-organizer', data=json.dumps(new_data) ,headers={'Authorization': f'Bearer {token}'} )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Organizer.objects.filter(organizer_name = "test").count(), 1)
        self.assertEqual(response.json().get('error', ''), 'Organizer name is already taken')
    
    def test_valid_revoke_organizer(self):
        normal_user = self.create_user("test1","test1", "win")
        organizer= self.become_organizer(normal_user, "test1", "organizer")
        token = self.get_token_for_user(normal_user)
        response = self.client.delete('/api/organizers/revoke-organizer', headers={'Authorization': f'Bearer {token}'} )
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.json()['success'], f'Organizer role revoked for user {normal_user.id}.')
        
    def test_invalid_revoke_organizer(self):
        normal_user = self.create_user("test1","test1", "win")
        token = self.get_token_for_user(normal_user)
        response = self.client.delete('/api/organizers/revoke-organizer', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 404)
        self.assertIn(response.json().get('error', ''), 'User is not an organizer')
        
    def test_valid_view_organizer(self):
        normal_user =self.create_user("test1","test1", "win")
        token = self.get_token_for_user(normal_user)
        organizer = self.become_organizer(normal_user, "test", "win")
        response = self.client.get("/api/organizers/view-organizer", headers={'Authorization': f'Bearer {token}'})
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
        response = self.client.post(
            f"/api/organizers/{organizer.id}/upload/logo/", 
            headers={'Authorization': f'Bearer {token}'}, 
            organizer_id = organizer.id,
            data = {'logo': image_file},
            format='multipart'
            )
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
        response = self.client.post(f"/api/organizers/{organizer.id}/upload/logo/", headers={'Authorization': f'Bearer {token}'}, organizer_id = organizer.id, data = {'logo': image_file})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), 'Invalid file type. Only JPEG and PNG are allowed.')
        
    def test_invalid_image_size(self):
        user = self.create_user("test","test","test")
        organizer = self.become_organizer(user,"test","test")
        token = self.get_token_for_user(user)
        image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'some content' * self.EXCEED_SIZE,
            content_type='image/png'
        )
        response = self.client.post(f"/api/organizers/{organizer.id}/upload/logo/", headers={'Authorization': f'Bearer {token}'}, organizer_id = organizer.id, data={'logo': image_file})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'File size exceeds the limit of 10.0 MB.')
        
    
    def test_set_new_image(self):
        user = self.create_user("test","test","test")
        token = self.get_token_for_user(user)
        organizer = self.become_organizer(user, "win", "win")
        image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'some content',
            content_type='image/png'
        )
        response = self.client.post(f"/api/organizers/{organizer.id}/upload/logo/", headers={'Authorization': f'Bearer {token}'}, organizer_id = organizer.id, data = {'logo': image_file})
    
    
    @patch("boto3.client")
    def test_upload_logo_image_s3_client_error(self, mock_boto_client):
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
        
        user = self.create_user("test","test","test")
        token = self.get_token_for_user(user)
        organizer = self.become_organizer(user, "win", "win")
  

        # Set up a mock image file
        image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'some content',
            content_type='image/png'
        )

        # Call the view that handles the S3 object deletion and upload
        token = self.get_token_for_user(self.test_user)
        response = self.client.post(f"/api/organizers/{organizer.id}/upload/logo/", 
                                    headers={'Authorization': f'Bearer {token}'},
                                    organizer_id = organizer.id, 
                                    data = {'logo': image_file})
        # Assert that the response has a 400 status code and contains the expected error messages
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Upload failed: An error occurred (InternalError) when calling the UploadFileObject operation: Internal error')

        # Assert that the delete_object and upload_fileobj methods were called as expected
        
        
        
    @patch('boto3.client')
    def test_general_exception_handling(self, mock_boto3_client):
        """Test general exception handling during upload"""
        # Mock S3 client to raise a general exception
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3
        mock_s3.upload_fileobj.side_effect = Exception("Unexpected error")
        
        user = self.create_user("test","test","test")
        token = self.get_token_for_user(user)
        organizer = self.become_organizer(user, "win", "win")
        
        image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'some content',
            content_type='image/png'
        )

        response = self.client.post(f"/api/organizers/{organizer.id}/upload/logo/", 
                                    headers={'Authorization': f'Bearer {token}'},
                                    organizer_id = organizer.id, 
                                    data = {'logo': image_file})

        self.assertEqual(response.status_code, 400)
        self.assertIn('Upload failed', response.json()['error'])


    def test_is_organizer(self):
        user = self.create_user("test","test","Test")
        token = self.get_token_for_user(user)
        organizer = self.become_organizer(user, "test","test123")
        self.assertTrue(organizer.is_organizer(user))
    

    def test_logo_url(self):
        user = self.create_user("test","test",'test')
        orgainzer = self.become_organizer(user, "test",'test123')
        organizer1 = Organizer.objects.create(
            user= user,
            organizer_name = "WwIN",
            email = str("win") + "@example.com",
            organization_type = "INDIVIDUAL",
        )
        self.assertEqual(type(orgainzer.logo_image_url) , str)
        self.assertEqual(organizer1.logo_image_url, None)
        