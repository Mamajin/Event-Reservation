from .utils.utils_comment import CommentModelsTest, Event, Http404, Comment
import json

class CommentTest(CommentModelsTest):
    
    
    
    def test_write_comment(self):
        user = self.create_user("test", "test", "test")
        token = self.get_token_for_user(user)
        data = {"content": "test description"}
        response = self.client.post(
            f"{self.write_comment_url}{self.event_test.id}",
            data=json.dumps(data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['content'], "test description")
    
  
    def test_raise_exception(self):
        user = self.create_user("test",'test', "test")
        token = self.get_token_for_user(user)
        non_exist_event = 0
        data = {'content' : "test description"}
        response = self.client.post(
            f"{self.write_comment_url}{non_exist_event}",
            data=json.dumps(data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], f"Event {non_exist_event} doesn't exist." )
        
        
    def test_delete_comment(self):
        user = self.create_user("test",'test',"test")
        token = self.get_token_for_user(user)
        data =  "test test"
        comment = self.create_comment(user , data)
        response = self.client.delete(f'/api/comments/{comment.id}/delete/',headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Delete comment successfully.')
        
    def test_invalid_delete_comment(self):
        user = self.create_user("test",'test',"win")
        user2= self.create_user("test123", "test123", "test")
        token = self.get_token_for_user(user)
        token2 = self.get_token_for_user(user2)
        data = "test test"
        comment = self.create_comment(user , data)
        response = self.client.delete(f'/api/comments/{comment.id}/delete/',headers={"Authorization": f"Bearer {token2}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['error'], 'You are not authorized to delete this comment' )
        
    def test_delete_does_not_exist_comment(self):
        user = self.create_user("test",'test',"win")
        token = self.get_token_for_user(user)
        response = self.client.delete(f'/api/comments/{0}/delete/',headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'Comment not found')
        
        
    def test_edit_comment(self):
        user = self.create_user("test", 'test', "test")
        token = self.get_token_for_user(user)
        comment = self.create_comment(user, content="Original content")
        
        # Data to update the comment
        data = {'content': "Updated content"}
        
        # Perform the PUT request to edit the comment
        response = self.client.put(f'/api/comments/{comment.id}/edit/', data=json.dumps(data), headers={"Authorization": f"Bearer {token}"})
        
        # Assert the status code is 200 (successful update)
        self.assertEqual(response.status_code, 200)
        
        # Assert that the comment content has been updated
        updated_comment = Comment.objects.get(id=comment.id)
        self.assertEqual(updated_comment.content, "Updated content")
        
        # Assert the response is correct
        self.assertEqual(response.json()['content'], "Updated content")
            
        
    def test_edit_comment_not_found(self):
        # Test case where the comment does not exist (invalid comment_id)
        user = self.create_user("test", 'test', "test")
        token = self.get_token_for_user(user)
        
        # Data to update the comment
        data = {'content': "Updated content"}
        
        # Perform the PUT request with a non-existing comment ID
        response = self.client.put(f'/api/comments/999999/edit/', data=json.dumps(data), headers={"Authorization": f"Bearer {token}"})
        
        # Assert the status code is 404 (not found)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'Comment not found')
        
        # Assert the error message
        
        
    def test_edit_comment_unauthorized(self):
        # Test case where the user tries to edit someone else's comment
        user1 = self.create_user("user1", 'user1', "test123")
        user2 = self.create_user("user2", 'user2', "test")
        token1 = self.get_token_for_user(user1)
        token2 = self.get_token_for_user(user2)
        
        # Create a comment by user1
        comment = self.create_comment(user1, content="Original content")
        
        # Data to update the comment
        data = {'content': "Updated content"}
        
        # Perform the PUT request to edit the comment by user2 (unauthorized)
        response = self.client.put(f'/api/comments/{comment.id}/edit/', data=json.dumps(data), headers={"Authorization": f"Bearer {token2}"})
        
        # Assert the status code is 403 (forbidden)
        self.assertEqual(response.status_code, 403)
        
        # Assert the error message
        self.assertEqual(response.json()['error'], 'Unauthorized to edit this comment')
        