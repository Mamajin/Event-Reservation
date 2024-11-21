from .modules import *
from django.contrib.auth.models import AnonymousUser
from typing import Union
from api.views.schemas.comment_schema import CommentResponseSchema
from api.views.schemas.event_schema import *
from api.views.schemas.ticket_schema import TicketResponseSchema
from api.views.schemas.user_schema import UserResponseSchema
from api.views.schemas.other_schema import ErrorResponseSchema, FileUploadResponseSchema
from .strategy.event_strategy import EventStrategy,EventEngagement



@api_controller('/events/', tags = ["Events"])
class EventAPI(ControllerBase):
    """
    API endpoints for event management.
    """
    @route.post('/create-event', response =EventResponseSchema, auth=JWTAuth())
    def create_event(self,request, data: EventInputSchema = Form(...), image: UploadedFile = File(None)):
        """
        Create a new event with optional image upload.

        Args:
            request (HttpRequest): The HTTP request object.
            data (EventInputSchema): Event data from the user.
            image (UploadedFile, optional): Image file for the event.

        Returns:
            EventResponseSchema: The created event details or error response.
        """
        strategy : EventStrategy= EventStrategy.get_strategy('create_event', request)
        return strategy.execute(data, image)

    @route.get('/my-events', response=List[EventResponseSchema], auth=JWTAuth())
    def get_my_events(self,request):
        """
        Retrieve events created by the logged-in organizer.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            List[EventResponseSchema]: List of events created by the organizer.
        """
        strategy : EventStrategy = EventStrategy.get_strategy('organizer_get_events', request)
        return strategy.execute()

    @route.get('/events', response=List[EventResponseSchema])
    def list_all_events(self,request: HttpRequest):
        """
        Retrieve all public events for the homepage.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            List[EventResponseSchema]: List of all events.
        """
        
        strategy : EventStrategy = EventStrategy.get_strategy('list_event', request)
        return strategy.execute()
    
    @route.patch('/{event_id}/edit', response={200: EventUpdateSchema, 401: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def edit_event(self,request: HttpRequest, event_id: int, data: EventUpdateSchema):
        """
        Edit an existing event by ID if the user is the organizer.

        Args:
            request (HttpRequest): The HTTP request object.
            event_id (int): ID of the event to edit.
            data (EventInputSchema): Updated event data.

        Returns:
            EventResponseSchema: Updated event details or error response.
        """
        strategy : EventStrategy = EventStrategy.get_strategy('edit_event', request)
        return strategy.execute(event_id, data)

    @route.get('/{event_id}', response=EventResponseSchema)
    def event_detail(self,request: HttpRequest, event_id: int):
        """
        Retrieve detailed information for a specific event.

        Args:
            request (HttpRequest): The HTTP request object.
            event_id (int): The ID of the event.

        Returns:
            EventResponseSchema: Details of the specified event.
        """
        strategy : EventStrategy = EventStrategy.get_strategy('event_detail', request)
        return strategy.execute(event_id)
        
    
    @route.post('/{event_id}/upload/event-image/', response={200: FileUploadResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())
    def upload_event_image(self,request: HttpRequest, event_id: int, file: UploadedFile = File(...)):
        """
        Upload an image for a specific event.

        Args:
            request (HttpRequest): The HTTP request object.
            event_id (int): The ID of the event to upload an image for.
            file (UploadedFile): Image file to upload.

        Returns:
            FileUploadResponseSchema: Details of the uploaded image, including URL, or an error response.
        """
        strategy : EventStrategy = EventStrategy.get_strategy('upload_event_image', request)
        return strategy.execute(event_id, file)
        
    
    @route.get('/{event_id}/comments', response=List[CommentResponseSchema])
    def get_events_comments(self, request: HttpRequest, event_id: int):
        """
        Retrieve all comments for a specific event, including nested replies.
        
        Args:
            request (HttpRequest): The HTTP request object, containing user and request metadata.
            event_id (int): The ID of the event for which comments are requested.

        Returns:
            Response (dict): A dictionary containing comments for the event.
        """
        strategy: EventEngagement = EventEngagement.get_engagement_strategy('event_comment', request, event_id)
        return strategy.execute()
    
    @route.get('/{event_id}/attendee-list', response=List[UserResponseSchema], auth=JWTAuth())
    def get_attendee_list(self, request: HttpRequest, event_id: int):
        """
        Retrieve the list of attendees for a specific event.

        Args:
            request (HttpRequest): The HTTP request object, containing user and request metadata.
            event_id (int): The ID of the event for which attendee list is requested.

        Returns:
            List[UserResponseSchema]: A list of attendee users for the event.
        """
        strategy : EventEngagement = EventEngagement.get_engagement_strategy('event_attendee', request, event_id)
        return strategy.execute()
        
    @route.get('/{event_id}/ticket-list', response=List[TicketResponseSchema], auth=JWTAuth())
    def get_ticket_list(self, request: HttpRequest, event_id: int):
        """
        Retrieve the list of tickets for a specific event.

        Args:
            request (HttpRequest): The HTTP request object, containing user and request metadata.
            event_id (int): The ID of the event for which ticket list is requested.

        Returns:
            List[TicketResponseSchema]: A list of tickets for the event.
        """
        strategy : EventEngagement = EventEngagement.get_engagement_strategy('event_ticket', request, event_id)
        return strategy.execute()    
    

