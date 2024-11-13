from .schemas import EventEngagementSchema, EventResponseSchema
from .modules import *


router = Router()


class LikeAPI:
    
    
    @router.put('/{event_id}/toggle-like', response={200: dict}, auth=JWTAuth())
    def toggle_like(request, event_id: int):
        user = request.user
        event = get_object_or_404(Event, id=event_id)

        try:
            like = Like.objects.get(event=event, user=user)
            like.status = 'unlike' if like.status == 'like' else 'like'
            like.save()
        except Like.DoesNotExist:
            like = Like.objects.create(event=event, user=user, status='like')
        
        # Return the updated user engagement status
        user_engaged = EventResponseSchema.resolve_user_engagement(event, user)
        return Response({"message": "Like toggled successfully.", "user_engaged": user_engaged}, status=200)

            