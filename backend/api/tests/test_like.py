from .utils.utils_like import LikeModelsTest, Like


class LikeTestAPI(LikeModelsTest):
    
    def test_toggle_like_on_new_event(self):
        token =self.get_token_for_user(self.test_user)
        response = self.client.put(f'/api/likes/{self.event_test.id}/toggle-like', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.first().status, 'like')
    def test_toggle_like_on_existing_event(self):
        Like.objects.create(event=self.event_test, user=self.test_user, status='like')
        token =self.get_token_for_user(self.test_user)
        response = self.client.put(f'/api/likes/{self.event_test.id}/toggle-like', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.first().status, 'unlike')
    def test_toggle_like_on_non_existent_event(self):
        token = self.get_token_for_user(self.test_user)
        response = self.client.put(f'/api/likes/{999}/toggle-like', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 404)

        
        
        