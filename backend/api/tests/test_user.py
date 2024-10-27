from api.urls import api  
from api.models import AttendeeUser, Organizer
from .utils.utils_user import UserModelsTest
from django.contrib.auth import authenticate
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth import get_user_model
from unittest.mock import Mock

User = get_user_model() 

class UserAPITests(UserModelsTest):
    
             
    def test_user_creation(self):
        response = self.client.post(self.user_create_url, data={
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
        response = self.client.post(self.user_create_url, data={
            'username': 'attendeeuser1',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'birth_date': '1995-06-15',
            'phone_number': '9876543210',
            'password': 'password123',
            'password2': 'password1234',
            'email': "jane@example.com"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Passwords do not match')
        same_user = self.create_user("test1","test1")
        response1 = self.client.post(self.user_create_url, data={
            'username': 'test1',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'birth_date': '1995-06-15',
            'phone_number': '9876543210',
            'password': 'password123',
            'password2': 'password123',
            'email': "jane@example.com"
        })
        self.assertEqual(response1.status_code,400)
        self.assertEqual(response1.json()['error'], 'Username already taken')
        
        
    # def test_login(self):
    #     user = User.objects.create_user(
    #         username="test",
    #         first_name="test",
    #         last_name='Doe',
    #         birth_date='1995-06-15',
    #         phone_number='9876543210',
    #         email='jane.doe@example.com',
    #         password='password123'  # Set the password here directly
    #     )
    #     data = {
    #         "username": user.username,
    #         "password": 'password123',
    #     }
    #     request = Mock()
    #     request.session = {}

    #     response = self.client.post(self.user_login_url, data= data)
    #     print(response.json())
        
    def test_if_user_is_organizer(self):
        normal_user = self.create_user("test","test")
        organizer = self.become_organizer(normal_user, "test")
        token = self.get_token_for_user(normal_user)
        response = self.client.get(self.user_profile_url, 
                                   headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.json()['status'], 'Organizer')
        
        
        
        
    def test_get_profile(self):
        token = self.get_token_for_user(self.test_user)
        response = self.client.get(self.user_profile_url, 
                                   headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], self.test_user.username)
        self.assertIn('status', response.json())
        
    
    def test_is_Attendeeuser(self):
        user = self.create_user("test","test_user")
        self.assertTrue(AttendeeUser.objects.filter(username = user.username))
        
    def test_is_Organizer(self):
        user = self.create_user("user_test", "test_user1")
        self.assertFalse(Organizer.objects.filter(user = user))
        organizer = self.become_organizer(user, "test_user")
        self.assertTrue(Organizer.objects.filter(organizer_name = organizer.organizer_name).exists())
        
    

        
        
        