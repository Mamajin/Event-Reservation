from .modules import *
from api.views.schemas.comment_schema import *
from api.views.schemas.other_schema import ErrorResponseSchema


router = Router()


class CommentAPI:
    
    @router.post('/write-comment/{event_id}', response={201: CommentResponseSchema, 400: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
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
        
        except Http404:
            logger.error(f"Event {event_id} doesn't exist.")
            return Response({'error': f"Event {event_id} doesn't exist."}, status=404)
        
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
        
        except Http404:
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

        except Http404:
            logger.error(f"Comment {comment_id} not found for edit.")
            return Response({'error': 'Comment not found'}, status=404)

        except Exception as e:
            logger.error(f"Error editing comment {comment_id}: {str(e)}")
            return Response({'error': str(e)}, status=500)
        
    @router.put('/{comment_id}/react/', response={200: dict, 404: ErrorResponseSchema}, auth=JWTAuth())
    def react_to_comment(request: HttpRequest,  comment_id: int, reaction: CommentType):
        """
        React to a comment with a specific reaction if user is authorized.

        Args:
            request (HttpRequest): HTTP request with authenticated user.
            comment_id (int): ID of the comment to react to.
            reaction (str): Reaction to apply.

        Returns:
            Response: Updated comment details or error if unauthorized/not found.
        """
        try:
            comment = get_object_or_404(Comment, id=comment_id)

            if reaction not in dict(CommentReaction.REACTION_CHOICES):
                logger.error(f"Invalid reaction type '{reaction}' by user {request.user.username}.")
                return Response({'error': 'Invalid reaction type.'}, status=400)

            existing_reaction = CommentReaction.objects.filter(
                comment=comment, user=request.user, reaction_type=reaction
            ).first()

            if not existing_reaction:
                CommentReaction.objects.create(
                    comment=comment, user=request.user, reaction_type=reaction
                )
                logger.info(f"User {request.user.username} added reaction '{reaction}' to comment {comment_id}.")
                return Response({'message': 'Reaction added successfully.'}, status=200)
            else:
                existing_reaction.delete()
                logger.info(f"User {request.user.username} removed reaction '{reaction}' from comment {comment_id}.")
                return Response({'message': 'Reaction removed successfully.'}, status=200)

        except Comment.DoesNotExist:
            logger.error(f"Comment {comment_id} not found for reaction.")
            return Response({'error': 'Comment not found.'}, status=404)
        except Exception as e:
            logger.error(f"Error reacting to comment {comment_id}: {str(e)}")
            return Response({'error': 'Internal server error.'}, status=500)
            