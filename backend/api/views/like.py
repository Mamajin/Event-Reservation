from .schemas import EventEngagementSchema, EventResponseSchema
from .modules import *


router = Router()


class LikeAPI:
    
    @router.post('/like', response={200: dict}, auth=JWTAuth())
    def like_event(request: HttpRequest, event_id: int):
        """_summary_

        Args:
            request (HttpRequest): _description_
            event_id (int): _description_
        """
        user = request.user
        event = get_object_or_404(Event, id=event_id)
        
        like, created = Like.objects.get_or_create(event=event, user=user)
        
        if created:
            return {"message": "Event liked successfully."}
        else:
            return {"message": "You have already liked this event."}
        
        
    @router.delete("/unlike", response={200: dict}, auth=JWTAuth())
    def unlike_event(request, event_id: int):
        user = request.user 
        event = get_object_or_404(Event, id=event_id)

        try:
            like = Like.objects.get(event=event, user=user)
            like.delete()
            return {"message": "Event unliked successfully."}
        except Like.DoesNotExist:
            return {"message": "You have not liked this event yet."}
            