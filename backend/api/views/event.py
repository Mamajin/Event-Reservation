from ninja import Router, Schema, NinjaAPI, Field
from ninja import NinjaAPI, Router, Schema, ModelSchema, Form
from typing import List, Optional
from api.models import *
from api.views.organizer import *
from ninja.responses import Response
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from datetime import datetime

logger = logging.getLogger(__name__)
router = Router()

class UserSchema(ModelSchema):
    class Meta:
        model = AttendeeUser
        fields = ['id', 'username', 'password','email'] 
        
 
class OrganizerSchema(ModelSchema):
    user : UserSchema
    
    class Meta:
        model = Organizer
        fields = ['user', 'organizer_name', 'email']


class EventSchema(ModelSchema):
    class Meta:
        model = Event
        fields = [
            'event_name',
            'event_create_date',
            'start_date_event',
            'end_date_event',
            'start_date_register',
            'end_date_register',
            'description',
            'max_attendee',
        ]
    

class EventResponseSchema(Schema):
    id: int
    organizer: OrganizerResponseSchema
    event_name: str
    event_create_date: datetime
    start_date_event: datetime
    end_date_event: datetime
    start_date_register: datetime
    end_date_register: datetime
    description: str
    max_attendee: int
                

class EventAPI:

    @router.post('/create-event', response=EventSchema, auth=JWTAuth())
    def create_event(request, data: EventSchema):
        this_user = request.user
        # Now, `user` will be the authenticated user.
        try:
            organizer = Organizer.objects.get(user=this_user)
        except Organizer.DoesNotExist:
            raise HttpError(status_code=403, message="You are not an organizer.")
        
        try:
            # Create the event
            event = Event.objects.create(
                event_name=data.event_name,
                organizer=organizer,  # Associate the organizer
                event_create_date=timezone.now(),  # Set creation date to current time
                start_date_event=data.start_date_event,
                end_date_event=data.end_date_event,
                start_date_register=data.start_date_register or timezone.now(),
                end_date_register=data.end_date_register,
                description=data.description,
                max_attendee=data.max_attendee
            )
        except Exception as e:
            raise HttpError(status_code=400, message=f"Failed to create event: {str(e)}")
        
        # Return the created event
        return event
        
    
    @router.get('/my-events', response=List[EventResponseSchema], auth=JWTAuth())
    def get_my_events(request: HttpRequest):
        """
        Retrieve a list of events created by the authenticated organizer.
        """
        if not request.user.is_authenticated:
            logger.warning(f"Unauthorized access to events by user: {request.user}")
            return Response({'error': 'User must be logged in'}, status=401)
        
        try:
            organizer = Organizer.objects.get(user=request.user)        
            events = Event.objects.filter(organizer=organizer)
            event_list = [
                EventResponseSchema(
                    id=event.id,
                    organizer=event.organizer,
                    event_name=event.event_name,
                    event_create_date=event.event_create_date,
                    start_date_event=event.start_date_event,
                    end_date_event=event.end_date_event,
                    start_date_register=event.start_date_register,
                    end_date_register=event.end_date_register,
                    description=event.description,
                    max_attendee=event.max_attendee
                )
                for event in events
            ]
            
            logger.info(f"Organizer {organizer.organizer_name} retrieved their events.")
            return event_list
        
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} tried to access events but is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=404)
        except Exception as e:
            logger.error(f"Error while retrieving events for organizer {request.user.id}: {str(e)}")
            return Response({'error': str(e)}, status=400)
        
    @router.get('/events', response=List[EventResponseSchema])
    def list_all_events(request: HttpRequest):
        """
        Retrieve a list of all events for the homepage.
        This endpoint is accessible to both authorized and unauthorized users.
        """
        try:
            events = Event.objects.all()
            event_list = [
                EventResponseSchema(
                    id=event.id,
                    organizer=event.organizer,
                    event_name=event.event_name,
                    event_create_date=event.event_create_date,
                    start_date_event=event.start_date_event,
                    end_date_event=event.end_date_event,
                    start_date_register=event.start_date_register,
                    end_date_register=event.end_date_register,
                    description=event.description,
                    max_attendee=event.max_attendee
                )
                for event in events
            ]

            logger.info("Retrieved all events for the homepage.")
            return event_list
        
        except Exception as e:
            logger.error(f"Error while retrieving events for the homepage: {str(e)}")
            return Response({'error': str(e)}, status=400)
        
    @router.put('/edit-event-{event_id}', response={204: None, 401: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def edit_event(request: HttpRequest, event_id: int, data: EventSchema):
        """Edit event detail by event ID."""
        if not request.user.is_authenticated:
            logger.warning(f"Unauthorized access to edit event by user: {request.user}")
            return Response({'error': 'User must be logged in'}, status=401)
        
        try:
            event = Event.objects.get(id=event_id)  
            organizer = Organizer.objects.get(user=request.user)
            if event.organizer != organizer:
                logger.warning(f"User {request.user.username} tried to edit an event they do not own.")
                return Response({'error': 'You are not allowed to edit this event.'}, status=403)
            
            event.event_name = data.event_name
            event.start_date_event = data.start_date_event
            event.end_date_event = data.end_date_event
            event.start_date_register = data.start_date_register or timezone.now()
            event.end_date_register = data.end_date_register
            event.description = data.description
            event.max_attendee = data.max_attendee
            
            event.save()
            
            logger.info(f"Organizer {organizer.organizer_name} edited their event {event_id}.")
            return Response(status=204) 
        
        except Event.DoesNotExist:
            logger.error(f"Event with ID {event_id} does not exist.")
            return Response({'error': 'Event not found'}, status=404)
        
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=404)
        
        except Exception as e:
            logger.error(f"Error while editing event {event_id}: {str(e)}")
            return Response({'error': str(e)}, status=400)
