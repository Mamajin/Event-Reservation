from .schemas import EventEngagementSchema, EventResponseSchema
from .modules import *
from api.views.strategy.like_strategy import *



@api_controller('/likes/', tags=['Likes'])
class LikeAPI:
    """Like an event."""
    
    @http_put('/{event_id}/toggle-like', response={200: dict}, auth=JWTAuth())
    def toggle_like(self, request: HttpRequest, event_id: int) -> dict:
        """Toggle the like status for a given event and user.

        Args:
            request (HttpRequest): The HTTP request containing the user information.
            event_id (int): The ID of the event to be liked or unliked.

        Returns:
            dict: A dictionary containing a success message and the user's engagement status.
        """
        strategy : LikeStrategy = LikeStrategy.get_strategy('like_event')
        return strategy.execute(request, event_id)
            