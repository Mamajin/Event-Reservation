from abc import ABC, abstractmethod
from api.views.modules import *
from api.views.schemas.event_schema import *

class BookmarkStrategy(ABC):
    """
    Abstract base class for event strategies.
    """
    def __init__(self, request: HttpRequest):
        self.user = request.user
    
    @staticmethod
    def get_strategy(strategy_name, request):
        """
        Retrieve the bookmark strategy instance based on the provided strategy name.

        Args:
            strategy_name (str): The name of the strategy to retrieve.
            request (HttpRequest): The HTTP request object, containing user and request metadata.

        Returns:
            An instance of the corresponding bookmark strategy class,
            or None if the strategy name is not found.
        """
        strategies = {
            'bookmark_show': BookmarkShowStrategy(request),
            'bookmark_toggle': BookmarkToggleStrategy(request),
        }
        return strategies.get(strategy_name)
    
    @abstractmethod
    def execute(self, *arg, **kwargs):
        """
        Execute the bookmark strategy with the given arguments.

        Args:
            *arg: Variable length argument list. The arguments passed to this method
                depend on the specific strategy being executed.
            **kwargs: Keyword argument dictionary. The keyword arguments passed to this
                method depend on the specific strategy being executed.

        Raises:
            NotImplementedError: If the execute method is not implemented in the derived class.
        """
        pass
    
    
    
class BookmarkShowStrategy(BookmarkStrategy):
    """Strategy for showing bookmarks."""
    def execute(self):
        """
        Retrieve and return a list of events bookmarked by the user.

        This method filters the bookmarks for the current user and collects the associated events.
        Engagement data and user engagement status are added to each event before returning the list.

        Returns:
            List[Dict]: A list containing event data with engagement and user engagement details.
        """
        bookmarks = Bookmarks.objects.filter(attendee=self.user)
        
        events = [bookmark.event for bookmark in bookmarks]

        # Add engagement and user_engaged properties
        event_data = []
        self.add_engagement(events, event_data)

        return event_data

    def add_engagement(self, events, event_data : list):
        """
        Add engagement and user engagement data to the given event data list.

        Args:
            events (List[Event]): The events to add engagement data for.
            event_data (List[Dict]): The list of event data to add the engagement data to.
        """
        for event in events:
            engagement = EventResponseSchema.resolve_engagement(event)
            user_engaged = EventResponseSchema.resolve_user_engagement(event, self.user)
            EventResponseSchema.set_status_event(event)
            event_schema = EventResponseSchema.from_orm(event)
            event_schema.engagement = engagement
            event_schema.user_engaged = user_engaged
            event_data.append(event_schema.dict())
            
            
class BookmarkToggleStrategy(BookmarkStrategy):
    """Strategy for toggling bookmarks."""
    def execute(self, event_id):
        """
        Toggle the bookmark status for the given event and user.

        Args:
            event_id (int): The ID of the event to bookmark or unbookmark.

        Returns:
            Response: A response containing a success message and the result of the operation.
        """
        
        event = get_object_or_404(Event, id=event_id)

        try:
            bookmark = Bookmarks.objects.get(event=event, attendee=self.user)
            bookmark.delete()
            return Response({"message": "Bookmark removed successfully."}, status=200)
        except Bookmarks.DoesNotExist:
            Bookmarks.objects.create(event=event, attendee=self.user)
            return Response({"message": "Bookmark added successfully."}, status=200)
    
        
    
    
    
