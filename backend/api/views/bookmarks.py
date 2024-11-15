from .modules import *
from .schemas import EventResponseSchema

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
        user = request.user
        bookmarks = Bookmarks.objects.filter(attendee=user)
        
        events = [bookmark.event for bookmark in bookmarks]


        event_data = [EventResponseSchema.from_orm(event).dict() for event in events]
        
        return event_data
    
    
    @router.put('/{event_id}/toggle-bookmark', auth=JWTAuth())
    def toggle_bookmark(request, event_id: int):
        """
        Toggle bookmark on an event. If the user has not bookmarked the event before, this will create a new bookmark.
        If the user has already bookmarked the event, this will toggle the bookmark status.
        """
        user = request.user
        event = get_object_or_404(Event, id=event_id)

        try:
            bookmark = Bookmarks.objects.get(event=event, attendee=user)
            bookmark.delete()
            return Response({"message": "Bookmark removed successfully."}, status=200)
        except Bookmarks.DoesNotExist:
            Bookmarks.objects.create(event=event, attendee=user)
            return Response({"message": "Bookmark added successfully."}, status=200)
    