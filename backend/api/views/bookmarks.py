from .modules import *
from .schemas import EventResponseSchema

router = Router()


class BookmarkAPI:
    
    @router.get('/my-favorite/', response=List[EventResponseSchema], auth=JWTAuth())
    def show_bookmark(request: HttpRequest):
        user = request.user
        bookmarks = Bookmarks.objects.filter(attendee=user)
        
        events = [bookmark.event for bookmark in bookmarks]


        event_data = [EventResponseSchema.from_orm(event).dict() for event in events]
        
        return event_data
    
    
    @router.post('/{event_id}/', auth= JWTAuth())
    def create_bookmark(request : HttpRequest, event_id : int):
        event = Event.objects.get(id = event_id)

        if Bookmarks.objects.filter(attendee = request.user, event = event).exists():
            return Response({'error': 'This event is already in your favorites'}, status = 400)
        
        user = request.user

        Bookmarks.objects.create(event = event, attendee = user)

        return Response({'success': 'This event has been added to your favorites.'}, status = 200)
    
    
    @router.delete('/{event_id}/remove', auth = JWTAuth())
    def delete_bookmark(request : HttpRequest, event_id : int):
        event = Event.objects.get(id = event_id)
        if Bookmarks.objects.filter(attendee = request.user , event = event_id).exists():
            bookmark = Bookmarks.objects.get(attendee = request.user , event = event)
            bookmark.delete()
            return Response({'success': 'This event has been removed from your favorites'}, status = 200)
        
        return Response({'error': 'You are not have permission to delete this'}, status = 404)
    
    



