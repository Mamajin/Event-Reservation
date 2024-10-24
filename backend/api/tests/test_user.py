from api.urls import api  
from api.models import AttendeeUser
from .utlis import BaseModelsTest, RefreshToken, AccessToken

class UserAPITests(BaseModelsTest):
    
    def get_token_for_user(self, user):
        """Helper method to generate a JWT token for the test user"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
            
        
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
        self.assertEqual(response.status_code, 200)
        user = AttendeeUser.objects.get(username = 'attendeeuser1')
        self.assertTrue(AttendeeUser.objects.filter(username = user.username).exists())
        
        
    def test_get_profile(self):
        token = self.get_token_for_user(self.test_user)
        response = self.client.get(self.user_profile_url, 
                                   headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], self.test_user.username)
        self.assertIn('status', response.json())
        
        