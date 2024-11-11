from .schemas import EventEngagementSchema, EventResponseSchema
from .modules import *


router = Router()


class LikeAPI:
    
    @router.post('/like/{event_id}', response={200: dict}, auth=JWTAuth())
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
            return Response({"success": "Event liked successfully."}, status = 200)
        else:
            return Response({"error": "You have already liked this event."}, status = 400)
        
        
    @router.delete("/unlike/{event_id}", response={200: dict}, auth=JWTAuth())
    def unlike_event(request, event_id: int):
        user = request.user 
        event = get_object_or_404(Event, id=event_id)
        try:
            like = Like.objects.get(event=event, user=user)
            like.delete()
            return Response({"message": "Event unliked successfully."}, status = 200)
        except Like.DoesNotExist:
            return Response({"message": "You have not liked this event yet."} , status = 400)
            