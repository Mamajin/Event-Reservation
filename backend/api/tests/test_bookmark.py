from .utils.utils_bookmark import BookmarkModelsTest, Bookmarks


class BookmarkTest(BookmarkModelsTest):
    
    def test_show_bookmark(self):
        token = self.get_token_for_user(self.test_user)
        response = self.client.get(self.show_bookmark_url, headers={"Authorization": f"Bearer {token}"})
        self.assertTrue(type(response.json()) == list)
        self.assertEqual(response.status_code, 200)
        
    
    def test_add_bookmark(self):
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        response = self.client.post(f'/{self.event_test.id}/', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code , 200)
        self.assertEqual(response.json()['success'], 'This event has been added to your favorites.')
        self.assertTrue(Bookmarks.objects.filter(event = self.event_test, attendee = user).exists())
        
    def test_user_already_bookmark(self):
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        bookmark = Bookmarks.objects.create(event = self.event_test, attendee = user)
        response = self.client.post(f'/{self.event_test.id}/', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code , 400)
        self.assertEqual(response.json()['error'], 'This event is already in your favorites')
        self.assertTrue(Bookmarks.objects.filter(event = self.event_test, attendee = user).exists())
        
        
        
    def test_delete_bookmark(self):
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        bookmark = Bookmarks.objects.create(event = self.event_test, attendee = user)
        response = self.client.delete(f'/{self.event_test.id}/remove', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code , 200)
        self.assertEqual(response.json()['success'],  'This event has been removed from your favorites')
        self.assertFalse(Bookmarks.objects.filter(event = self.event_test, attendee = user).exists())
        
        
    def test_invalid_delete_bookmark(self):
        user = self.create_user("test","test")
        token = self.get_token_for_user(user)
        response = self.client.delete(f'/{self.event_test.id}/remove', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code , 404)
        self.assertEqual(response.json()['error'],  'You are not have permission to delete this')
        self.assertFalse(Bookmarks.objects.filter(event = self.event_test, attendee = user).exists())
        