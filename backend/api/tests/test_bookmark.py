from .utils.utils_bookmark import BookmarkModelsTest, Bookmarks


class BookmarkTest(BookmarkModelsTest):
    
    def test_show_bookmark(self):
        token = self.get_token_for_user(self.test_user)
        response = self.client.get(self.show_bookmark_url, headers={"Authorization": f"Bearer {token}"})
        self.assertTrue(type(response.json()) == list)
        self.assertEqual(response.status_code, 200)
        

    def test_toggle_bookmark_not_bookmarked(self):
        token = self.get_token_for_user(self.test_user)
        response = self.client.put(f'/api/bookmarks/{self.event_test.id}/toggle-bookmark',headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Bookmark added successfully.')
        self.assertEqual(Bookmarks.objects.filter(event=self.event_test, attendee=self.test_user).count(), 1)

    def test_toggle_bookmark_already_bookmarked(self):
        Bookmarks.objects.create(event=self.event_test, attendee=self.test_user)
        token = self.get_token_for_user(self.test_user)
        response = self.client.put(f'/api/bookmarks/{self.event_test.id}/toggle-bookmark',headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Bookmark removed successfully.')
        self.assertEqual(Bookmarks.objects.filter(event=self.event_test, attendee=self.test_user).count(), 0)

    def test_toggle_bookmark_event_does_not_exist(self):
        token = self.get_token_for_user(self.test_user)
        response = self.client.put(f'/api/bookmarks/{999}/toggle-bookmark',headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)

  