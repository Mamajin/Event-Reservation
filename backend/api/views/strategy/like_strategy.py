from abc import ABC, abstractmethod
from api.views.modules import *
from api.views.schemas.event_schema import EventResponseSchema


class LikeStrategy(ABC):
    """
    Like strategy.
    """
    
    @staticmethod
    def get_strategy(strategy_name):
        """Get the strategy based on the strategy name."""
        strategies = {
            'like_event': LikeEventStrategy()
            }
        return strategies.get(strategy_name)
    
    @abstractmethod
    def execute(self, *arg, **kwargs):
        """Execute the strategy"""
        pass
    
    
class LikeEventStrategy(LikeStrategy):
    """Like event strategy."""
    def execute(self, request, event_id):
        """Toggle the like status for a given event and user.

        Args:
            request (HttpRequest): The HTTP request containing the user information.
            event_id (int): The ID of the event to be liked or unliked.

        Returns:
            Response: A response containing a success message and the user's engagement status.
        """
        user = request.user
        event = get_object_or_404(Event, id=event_id)

        try:
            like = Like.objects.get(event=event, user=user)
            like.status = 'unlike' if like.status == 'like' else 'like'
            like.save()
            like.refresh_from_db()
        except Like.DoesNotExist:
            like = Like.objects.create(event=event, user=user, status='like')
            like.refresh_from_db()
        
        user_engaged = EventResponseSchema.resolve_user_engagement(event, user)
        return Response({"message": "Like toggled successfully.", "user_engaged": user_engaged}, status=200)
