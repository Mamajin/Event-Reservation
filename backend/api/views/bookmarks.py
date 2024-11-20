from .modules import *
from api.views.schemas.event_schema import EventResponseSchema
from api.views.strategy.bookmark_strategy import BookmarkStrategy


@api_controller('/bookmarks', tags=['Bookmarks'])
class BookmarkAPI:
    """
    API endpoints for managing bookmarks.
    """
    @route.get('/my-favorite/', response=List[EventResponseSchema], auth=JWTAuth())
    def show_bookmark(self, request: HttpRequest):
        """
        Retrieves a list of events that are bookmarked by the authenticated user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            List[EventResponseSchema]: A list of event data in the form of EventResponseSchema.
        """
        strategy : BookmarkStrategy = BookmarkStrategy.get_strategy('bookmark_show', request)
        return strategy.execute()
    
    @route.put('/{event_id}/toggle-bookmark', auth=JWTAuth())
    def toggle_bookmark(self, request, event_id: int):
        """
        Toggles the bookmark status for a given event and user.

        Args:
            request (HttpRequest): The HTTP request object.
            event_id (int): The ID of the event to be bookmarked or unbookmarked.

        Returns:
            Response: A response containing a success message and the user's bookmark status.
        """
        strategy : BookmarkStrategy = BookmarkStrategy.get_strategy('bookmark_toggle', request)
        return strategy.execute(event_id)
    