from .schemas import EventEngagementSchema, EventResponseSchema
from .modules import *


router = Router()


class LikeAPI:
    
    
    @router.put('/{event_id}/toggle-like', response={200: dict}, auth=JWTAuth())
    def toggle_like(request, event_id: int):
        """
        Toggle like on an event. If the user has not liked the event before, this will create a new like.
        If the user has already liked the event, this will toggle the like status.
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

        return Response({"message": "Like toggled successfully."}, status=200)
            