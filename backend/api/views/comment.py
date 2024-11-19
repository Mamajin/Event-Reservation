from .modules import *
from api.views.schemas.comment_schema import *
from api.views.schemas.other_schema import ErrorResponseSchema
from api.views.strategy.comment_strategy import CommentStrategy


@api_controller('/comments/', tags=['Comments'])
class CommentAPI:
    
    @http_post('/write-comment/{event_id}', response={201: dict}, auth=JWTAuth())
    def create_comment(self, request: HttpRequest, event_id: int, comment: CommentSchema):
        """Create a new comment for a specific event.

        Args:
            request (HttpRequest): HTTP request with authenticated user.
            event_id (int): ID of the event to comment on.
            comment (CommentSchema): Comment data including content and optional parent ID.

        Returns:
            Response: Created comment details or error message.
        """
        strategy : CommentStrategy = CommentStrategy.get_strategy('create_comment')
        return strategy.execute(request, event_id, Comment)
        
    @http_delete('/{comment_id}/delete/', response={200: dict, 404: ErrorResponseSchema}, auth=JWTAuth())
    def delete_comment(self, request: HttpRequest, comment_id: int):
        """Delete a comment by ID if user is authorized.

        Args:
            request (HttpRequest): HTTP request with authenticated user.
            comment_id (int): ID of the comment to delete.

        Returns:
            Response: Success message or error if unauthorized/not found.
        """
        strategy : CommentStrategy = CommentStrategy.get_strategy('delete_comment')
        return strategy.execute(request, comment_id)
            
    @http_put('/{comment_id}/edit/', response={200: dict, 404: ErrorResponseSchema}, auth=JWTAuth())
    def edit_comment(self, request: HttpRequest, comment_id: int, data: CommentSchema):
        """Edit a comment's content if user is authorized.

        Args:
            request (HttpRequest): HTTP request with authenticated user.
            comment_id (int): ID of the comment to edit.
            data (CommentSchema): Updated comment content.

        Returns:
            Response: Updated comment details or error if unauthorized/not found.
        """
        strategy : CommentStrategy = CommentStrategy.get_strategy('update_comment')
        return strategy.execute(request, comment_id, data)
        
    @http_put('/{comment_id}/react/', response={200: dict, 404: ErrorResponseSchema}, auth=JWTAuth())
    def react_to_comment(self, request: HttpRequest,  comment_id: int, reaction: CommentType):
        """React to a comment with a specific reaction if user is authorized.

        Args:
            request (HttpRequest): HTTP request with authenticated user.
            comment_id (int): ID of the comment to react to.
            reaction (str): Reaction to apply.

        Returns:
            Response: Updated comment details or error if unauthorized/not found.
        """
        strategy : CommentStrategy = CommentStrategy.get_strategy('comment_reactions')
        return strategy.execute(request, comment_id, reaction)