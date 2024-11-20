from .modules import *
from api.views.schemas.event_schema import EventResponseSchema
from .strategy.bookmark_strategy import BookmarkStrategy


router = Router()


class BookmarkAPI:
    
    @router.get('/my-favorite/', response=List[EventResponseSchema], auth=JWTAuth())
    def show_bookmark(request: HttpRequest):
        """
        Retrieves a list of events that are bookmarked by the authenticated user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            List[EventResponseSchema]: A list of event data in the form of EventResponseSchema.
        """
        strategy : BookmarkStrategy = BookmarkStrategy.get_strategy('bookmark_show', request)
        return strategy.execute()
    
    @router.put('/{event_id}/toggle-bookmark', auth=JWTAuth())
    def toggle_bookmark(request, event_id: int):
        """
        Toggle bookmark on an event. If the user has not bookmarked the event before, this will create a new bookmark.
        If the user has already bookmarked the event, this will toggle the bookmark status.
        """
        straegy : BookmarkStrategy = BookmarkStrategy.get_strategy('bookmark_toggle', request)
        return straegy.execute(event_id)
    