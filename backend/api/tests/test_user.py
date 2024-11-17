from decimal import Decimal
from api.urls import api  
from api.models import AttendeeUser, Organizer
from api.utils import EmailVerification
from .utils.utils_user import UserModelsTest, SimpleUploadedFile, ClientError
from django.contrib.auth import authenticate
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user
from unittest.mock import Mock, patch, MagicMock
from google.oauth2 import id_token
from django.utils import timezone
from requests import Request

User = get_user_model() 

class UserAPITests(UserModelsTest):
    
             
    def test_user_creation(self):
        response = self.client.post('/api/users/register', data={
            'username': 'attendeeuser1',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'birth_date': '1995-06-15',
            'phone_number': '9876543210',
            'password': 'password123',
            'password2': 'password123',
            'email': "jane@example.com"
        })
        self.assertEqual(response.status_code, 201)
        user = AttendeeUser.objects.get(username = 'attendeeuser1')
        self.assertTrue(AttendeeUser.objects.filter(username = user.username).exists())
        
    def test_invalid_creation(self):
        response = self.client.post('/api/users/register', data={
            'username': 'attendeeuser1',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'birth_date': '1995-06-15',
            'phone_number': '9876543210',
            'password': 'password123',
            'password2': 'password1234',
            'email': "jane123@example.com"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Passwords do not match')
        same_user = self.create_user("test1","test1", "win")
        response1 = self.client.post('/api/users/register', data={
            'username': 'test1',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'birth_date': '1995-06-15',
            'phone_number': '9876543210',
            'password': 'password123',
            'password2': 'password123',
            'email': "jane1234@example.com"
        })
        self.assertEqual(response1.status_code,400)
        self.assertEqual(response1.json()['error'], 'Username already taken')
        same_emal_user=  self.create_user("win","win","jane1234")
        response2 = self.client.post('/api/users/register', data={
            'username': 'test123',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'birth_date': '1995-06-15',
            'phone_number': '9876543210',
            'password': 'password123',
            'password2': 'password123',
            'email': "jane1234@example.com"
        })
        self.assertTrue(response2.status_code, 400)
        self.assertEqual(response2.json()['error'], 'This email already taken')
        
    def test_invalid_phone_number(self):
        response = self.client.post('/api/users/register', data={
            'username': 'attendeeuser1',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'birth_date': '1995-06-15',
            'phone_number': '987654321011',
            'password': 'password123',
            'password2': 'password123',
            'email': "jane@example.com"
        })
        self.assertEqual(response.json()['error'], 'Phone number must be 10 digits long')
        self.assertEqual(response.status_code, 400)
        response1 = self.client.post('/api/users/register', data={
            'username': 'attendeeuser1',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'birth_date': '1995-06-15',
            'phone_number': '9876543abc',
            'password': 'password123',
            'password2': 'password123',
            'email': "jane@example.com"
        })
        self.assertEqual(response1.json()['error'], 'Phone number must be digit')
        self.assertEqual(response1.status_code, 400)
        
    
        
    def test_get_profile(self):
        token = self.get_token_for_user(self.test_user)
        response = self.client.get('/api/users/profile', 
                                   headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], self.test_user.username)
        self.assertIn('status', response.json())
        
        
    def test_edit_profile(self):
        user = self.create_user("test","test",'test')
        token = self.get_token_for_user(user)
        data= {
                "id": user.id,
                "username": "string",
                "first_name": "win",
                "last_name": "string",
                "birth_date": "2024-11-09",
                "phone_number": "string",
                "email": "user@example.com",
                "status": "string",
                "address": "string",
                "latitude": 0,
                "longitude": 0,
                "profile_picture": "string",
                "company": "string",
                "facebook_profile": "string",
                "instagram_handle": "string",
                "nationality": "string",
                "attended_events_count": 0,
                "cancelled_events_count": 0,
                "created_at": "2024-11-09T10:10:45.762Z",
                "updated_at": "2024-11-09T10:10:45.762Z"
            }
    
        response = self.client.patch('/api/users/edit-profile/' + f"{user.id}/", 
                                   headers={"Authorization": f"Bearer {token}"}, json = data)
        user.refresh_from_db()
        self.assertTrue(AttendeeUser.objects.filter(first_name = user.first_name).exists())
        self.assertTrue(response.status_code , 200)
        
        
    def test_delete_user(self):
        user = self.create_user("test","test","test")
        token = self.get_token_for_user(user)
        response = self.client.delete('/api/users/delete/', 
                                   headers={"Authorization": f"Bearer {token}"})
        self.assertTrue(response.status_code, 200)
        self.assertFalse(AttendeeUser.objects.filter(username = user.username).exists())
        self.assertEqual(response.json()['success'], 'Your account has been deleted')
        
        
    def test_upload_image(self):
        user = self.create_user("test","test","test")
        token = self.get_token_for_user(user)
        
        image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'some content',
            content_type='image/png'
        )
        response = self.client.post(f'/api/users/{user.id}/upload/profile-picture/', 
                                   headers={"Authorization": f"Bearer {token}"}, data = {'profile_picture': image_file})
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Upload successful')
        
    def test_invalid_upload_image(self):
        user = self.create_user("test","test","test")
        token = self.get_token_for_user(user)
        
        image_file = SimpleUploadedFile(
            name='test_image.gif',
            content=b'some content',
            content_type='image/gif'
        )
        response = self.client.post(f"/api/users/{user.id}/upload/profile-picture/", 
                                   headers={"Authorization": f"Bearer {token}"}, data = {'profile_picture': image_file})
        
        self.assertTrue(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid file type. Only JPEG and PNG are allowed.')
        exceed_size_image = SimpleUploadedFile(
            name='test_image.png',
            content=b'some content' * 10 * 1024 * 1024,
            content_type='image/png'
        )
        response1 = self.client.post(f"/api/users/{user.id}/upload/profile-picture/", 
                                   headers={"Authorization": f"Bearer {token}"}, data = {'profile_picture': exceed_size_image})
        
        self.assertTrue(response1.status_code, 400)
        self.assertEqual(response1.json()['error'],'File size exceeds the limit of 10.0 MB.' )
        
        
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
        organizer = self.become_organizer(user, "win")
  

        # Set up a mock image file
        image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'some content',
            content_type='image/png'
        )

        # Call the view that handles the S3 object deletion and upload
        token = self.get_token_for_user(self.test_user)
        response = self.client.post(f"/api/users/{user.id}/upload/profile-picture/", 
                                   headers={"Authorization": f"Bearer {token}"}, data = {'profile_picture': image_file})
    
        # Assert that the response has a 400 status code and contains the expected error messages
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'S3 upload failed: An error occurred (InternalError) when calling the UploadFileObject operation: Internal error')
        

        
    @patch('boto3.client')
    def test_general_exception_handling(self, mock_boto3_client):
        """Test general exception handling during upload"""
        # Mock S3 client to raise a general exception
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3
        mock_s3.upload_fileobj.side_effect = Exception("Unexpected error")
        
        user = self.create_user("test","test","test")
        token = self.get_token_for_user(user)
        
        image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'some content',
            content_type='image/png'
        )

        response = self.client.post(f"/api/users/{user.id}/upload/profile-picture/", 
                                   headers={"Authorization": f"Bearer {token}"}, data = {'profile_picture': image_file})
    

        self.assertEqual(response.status_code, 400)
        self.assertIn('Upload failed', response.json()['error'])
        
        
    @patch.object(EmailVerification, 'send_verification_email')
    
    def test_resend_verification_unverified_user(self, mock_send_verification_email):
        user = self.create_user("test","test","test")

        response = self.client.post('/api/users/resend-verification?email=test@example.com')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Verification email sent successfully')
        
        response1 = self.client.post('/api/users/resend-verification?email=verification@example.com')
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response1.json()['error'], "User not found or already verified")
        
        mock_send_verification_email.assert_called_once()

        
