from  .schemas import CommentSchema, CommentResponseSchema, CommentReaction, ErrorResponseSchema
from .modules import *


router = Router()


class CommentAPI:
    
    @router.post('/write-comment/', response={201: CommentResponseSchema, 400: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def create_comment(request: HttpRequest, event_id: int, comment: CommentSchema):
        """
        Create a new comment for a specific event.

        Args:
            request (HttpRequest): HTTP request with authenticated user.
            event_id (int): ID of the event to comment on.
            comment (CommentSchema): Comment data including content and optional parent ID.

        Returns:
            Response: Created comment details or error message.
        """
        try:
            user = request.user
            event = get_object_or_404(Event, id=event_id)
            parent_comment = Comment.objects.filter(id=comment.parent_id).first() if comment.parent_id else None
            
            logger.info(f"User {user.username} attempted to comment.")
            comment = Comment.objects.create(
                event=event, user=user, parent=parent_comment,
                content=comment.content, status=Comment.Status.APPROVED
            )
            logger.info(f"Comment created for event {event_id} by {user.username}.")
            return Response(CommentResponseSchema.from_orm(comment), status=200)
        
        except Event.DoesNotExist:
            logger.error(f"Event {event_id} doesn't exist.")
            return Response({'error': "Event {event_id} doesn't exist."}, status=404)
        
    @router.delete('/{comment_id}/delete/', response={204: None, 404: ErrorResponseSchema}, auth=JWTAuth())
    def delete_comment(request: HttpRequest, comment_id: int):
        """
        Delete a comment by ID if user is authorized.

        Args:
            request (HttpRequest): HTTP request with authenticated user.
            comment_id (int): ID of the comment to delete.

        Returns:
            Response: Success message or error if unauthorized/not found.
        """
        try:
            comment = get_object_or_404(Comment, id=comment_id)
            if comment.user != request.user:
                logger.warning(f"Unauthorized delete attempt by '{request.user.username}' on comment {comment_id}.")
                return Response({
                    'error': 'You are not authorized to delete this comment'
                }, status=403)
                
            comment.delete()
            logger.info(f"Comment {comment_id} deleted by user {request.user.username}")
            return Response({'message': 'Delete comment successfully.'}, status=204)
        
        except Comment.DoesNotExist:
            logger.error(f"Comment {comment_id} not found for deletion.")
            return Response({'error': 'Comment not found'}, status=404)
            
    @router.put('/{comment_id}/edit/', response={200: CommentResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def edit_comment(request: HttpRequest, comment_id: int, data: CommentSchema):
        """
        Edit a comment's content if user is authorized.

        Args:
            request (HttpRequest): HTTP request with authenticated user.
            comment_id (int): ID of the comment to edit.
            data (CommentSchema): Updated comment content.

        Returns:
            Response: Updated comment details or error if unauthorized/not found.
        """
        try:
            comment = get_object_or_404(Comment, id=comment_id)

            if comment.user != request.user:
                logger.warning(f"Unauthorized edit attempt by '{request.user.username}' on comment {comment_id}.")
                return Response({'error': 'Unauthorized to edit this comment'}, status=403)

            comment.content = data.content
            comment.save(update_fields=['content'])

            logger.info(f"Comment {comment_id} edited by user {request.user.username}")
            return Response(CommentResponseSchema.from_orm(comment), status=200)

        except Comment.DoesNotExist:
            logger.error(f"Comment {comment_id} not found for edit.")
            return Response({'error': 'Comment not found'}, status=404)

            