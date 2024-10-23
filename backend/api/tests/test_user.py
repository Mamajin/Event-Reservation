from api.urls import api  
from api.models import AttendeeUser
from .utlis import BaseModelsTest

class UserAPITests(BaseModelsTest):
    def test_user_creation(self):
        response = self.client.post(self.user_create_url, data={
            'username': 'attendeeuser1',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'birth_date': '1995-06-15',  # Correctly formatted date string
            'phone_number': '9876543210',
            'password': 'password123',
            'password2': 'password123',
            'email': "jane@example.com"# Ensure this matches password
        })
        self.assertEqual(response.status_code, 200)
        user = AttendeeUser.objects.get(username = 'attendeeuser1')
        self.assertTrue(AttendeeUser.objects.filter(username = user.username).exists())
        
        
    
        