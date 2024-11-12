from .utils.utils_like import LikeModelsTest, Like


class LikeTestAPI(LikeModelsTest):
    
    def test_user_like(self):
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        response = self.client.post(self.user_like_url + f"{self.event_test.id}",headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'],'Event liked successfully.')
        
    def test_user_already_like(self):
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        like = Like.objects.create(user = user , event = self.event_test)
        response = self.client.post(self.user_like_url + f"{self.event_test.id}",headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code , 400)
        self.assertEqual(response.json()['error'], 'You have already liked this event.')
        
        
    def test_user_unlike_the_event_that_did_not_like(self):
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        response = self.client.delete(self.user_unlike_url + f"{self.event_test.id}",headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'You have not liked this event yet.')
        
        
    def test_user_unlike(self):
        user1 = self.create_user("test123","test")
        token1 = self.get_token_for_user(user1)
        like = Like.objects.create(user = user1 , event = self.event_test)
        response = self.client.delete(self.user_unlike_url + f"{self.event_test.id}",headers={"Authorization": f"Bearer {token1}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Event unliked successfully.')
        
        
        
        