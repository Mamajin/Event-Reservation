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
    
    
    @router.post('/{event_id}/', auth=JWTAuth())
    def create_bookmark(request : HttpRequest, event_id : int):
        """
        Creates a new bookmark for a specific event if it does not already exist.

        Args:
            request (HttpRequest): The HTTP request object containing the authenticated user.
            event_id (int): The ID of the event to be bookmarked.

        Returns:
            Response: A success message if the bookmark is created, or an error message if the event is already bookmarked.
        """
        event = Event.objects.get(id = event_id)

        if Bookmarks.objects.filter(attendee = request.user, event = event).exists():
            return Response({'error': 'This event is already in your favorites'}, status = 400)
        
        user = request.user

        Bookmarks.objects.create(event = event, attendee = user)

        return Response({'success': 'This event has been added to your favorites.'}, status = 200)
    
    
    @router.delete('/{event_id}/remove', auth=JWTAuth())
    def delete_bookmark(request: HttpRequest, event_id: int):
        """
        Delete a bookmark for a specific event if the user has permission.

        Args:
            request (HttpRequest): HTTP request with authenticated user.
            event_id (int): ID of the event to remove from bookmarks.

        Returns:
            Response: Success message if the bookmark is deleted, 
                      error message if the user doesn't have permission.
        """
        event = Event.objects.get(id=event_id)        
        if Bookmarks.objects.filter(attendee=request.user, event=event).exists():
            bookmark = Bookmarks.objects.get(attendee=request.user, event=event)
            bookmark.delete()            
            return Response({'success': 'This event has been removed from your favorites'}, status=200)        
        return Response({'error': 'You do not have permission to delete this'}, status=404)
    
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
    