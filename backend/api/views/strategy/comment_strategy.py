from abc import ABC, abstractmethod
from api.views.modules import *
from api.views.schemas.comment_schema import CommentResponseSchema, CommentSchema


class CommentStrategy(ABC):
    """
    Abstract base class for comment strategies.
    """
    @staticmethod
    def get_strategy(strategy_name):
        """Get the strategy based on the strategy name."""
        strategies = {
            'create_comment': CommentCreateStrategy(),
            'update_comment': CommentUpdateStrategy(),
            'delete_comment': CommentDeleteStrategy(),
        }
        return strategies.get(strategy_name)
    
    @abstractmethod
    def execute(self, *arg, **kwargs):
        """Execute the strategy."""
        pass
    

class CommentCreateStrategy(CommentStrategy):
    """Create a new comment for a specific event."""
    def execute(self, request: HttpRequest, event_id: int, comment: CommentSchema):
        """Create a new comment for a specific event.

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
        
        except Http404:
            logger.error(f"Event {event_id} doesn't exist.")
            return Response({'error': f"Event {event_id} doesn't exist."}, status=404)
        except Exception as e:
            logger.error(f"Error creating comment for event {event_id}: {str(e)}")
            return Response({'error': str(e)}, status=500)
        
        
class CommentUpdateStrategy(CommentStrategy):
    """Update a comment by ID."""
    def execute(self, request: HttpRequest, comment_id: int, data: CommentSchema):
        """Update a comment by ID.

        Args:
            request (HttpRequest): HTTP request with authenticated user.
            comment_id (int): ID of the comment to update.
            comment (CommentSchema): Updated comment content.

        Returns:
            Response: Updated comment details or error message.
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

        except Http404:
            logger.error(f"Comment {comment_id} not found for edit.")
            return Response({'error': 'Comment not found'}, status=404)

        except Exception as e:
            logger.error(f"Error editing comment {comment_id}: {str(e)}")
            return Response({'error': str(e)}, status=500)
        
        
        
class CommentDeleteStrategy(CommentStrategy):
    """Delete a comment by ID."""
    def execute(self, request: HttpRequest, comment_id: int):
        """Delete a comment by ID.

        Args:
            request (HttpRequest): HTTP request with authenticated user.
            comment_id (int): ID of the comment to delete.

        Returns:
            Response: Success message or error message.
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
            return Response({'message': 'Delete comment successfully.'}, status=200)
        
        except Http404:
            logger.error(f"Comment {comment_id} not found for delete.")
            return Response({'error': 'Comment not found'}, status=404)
        