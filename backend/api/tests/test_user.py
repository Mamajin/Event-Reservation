from api.urls import api  
from api.models import AttendeeUser, Organizer
from .utils.utils_user import UserModelsTest


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
        
    
    def test_is_Attendeeuser(self):
        user = self.create_user("test","test_user")
        self.assertTrue(AttendeeUser.objects.filter(username = user.username))
        
    def test_is_Organizer(self):
        user = self.create_user("user_test", "test_user1")
        self.assertFalse(Organizer.objects.filter(user = user))
        organizer = self.become_organizer(user, "test_user")
        self.assertTrue(Organizer.objects.filter(organizer_name = organizer.organizer_name).exists())
        
    

        
        
        