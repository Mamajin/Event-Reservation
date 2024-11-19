from abc import ABC, abstractmethod
from api.views.modules import *
from api.views.schemas import *

class BookmarkStrategy(ABC):
    
    def __init__(self, request: HttpRequest):
        self.user = request.user
    
    @staticmethod
    def get_strategy(strategy_name, request):
        strategies = {
            'bookmark_show': BookmarkShowStrategy(request),
            'bookmark_toggle': BookmarkToggleStrategy(request),
        }
        return strategies.get(strategy_name)
    
    @abstractmethod
    def execute(self, *arg, **kwargs):
        pass
    
    
    
class BookmarkShowStrategy(BookmarkStrategy):
    
    def execute(self):
        bookmarks = Bookmarks.objects.filter(attendee=self.user)
        
        events = [bookmark.event for bookmark in bookmarks]

        # Add engagement and user_engaged properties
        event_data = []
        self.add_engagement(events, event_data)

        return event_data

    def add_engagement(self, events, event_data : list):
        for event in events:
            engagement = EventResponseSchema.resolve_engagement(event)
            user_engaged = EventResponseSchema.resolve_user_engagement(event, self.user)
            EventResponseSchema.set_status_event(event)
            event_schema = EventResponseSchema.from_orm(event)
            event_schema.engagement = engagement
            event_schema.user_engaged = user_engaged
            event_data.append(event_schema.dict())
            
            
class BookmarkToggleStrategy(BookmarkStrategy):
    
    def execute(self, event_id):
        event = get_object_or_404(Event, id=event_id)

        try:
            bookmark = Bookmarks.objects.get(event=event, attendee=self.user)
            bookmark.delete()
            return Response({"message": "Bookmark removed successfully."}, status=200)
        except Bookmarks.DoesNotExist:
            Bookmarks.objects.create(event=event, attendee=self.user)
            return Response({"message": "Bookmark added successfully."}, status=200)
    
        
    
    
    
