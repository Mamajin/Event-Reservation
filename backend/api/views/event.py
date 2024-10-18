from ninja import Router, Schema, NinjaAPI, Field
from django.utils.decorators import method_decorator
from ninja import Router, Schema, ModelSchema, Form
from typing import List, Optional
from api.models import *
from api.views.organizer import *
from django.contrib.auth.decorators import login_required
from pydantic import field_validator
from datetime import datetime
from ninja.responses import Response
from rest_framework import status
import logging


logger = logging.getLogger(__name__)
router = Router()


class EventSchema(ModelSchema):
    event_name: str
    start_date_event: datetime
    end_date_event: datetime
    start_date_register: datetime
    end_date_register: datetime
    description: Optional[str]
    max_attendee: int

    class Config:
        model = Event
        model_fields = ['event_name', 'start_date_event', 'end_date_event',
                         'start_date_register', 'end_date_register',
                           'description', 'max_attendee']
        

class EventResponseSchema(ModelSchema):
    organizer: OrganizerSchema
    class Config:
        model = Event
        model_fields = '__all__'


class EditEventSchema(Schema):
    event_name: Optional[str] = None
    start_date_event: Optional[datetime] = None
    end_date_event: Optional[datetime] = None
    start_date_register: Optional[datetime] = None
    end_date_register: Optional[datetime] = None
    description: Optional[str] = None
    max_attendee: Optional[int] = None



class EventAPI:
    
    @router.post('/create-event', response=EventResponseSchema)
    def create_event(request, form: EventSchema):
        this_user = request.user
        logger.debug(f"Attempt to create event by user: {this_user.username}")
    
        try:
            organizer = Organizer.objects.get(user=this_user)
        except Organizer.DoesNotExist:
            logger.error(f"Organizer not found for user: {this_user}")
            return Response({'error': 
                    'Organizer does not exist.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            event = Event.objects.create(
                organizer=organizer,
                event_name=form.event_name,
                start_date_event=form.start_date_event,
                end_date_event=form.end_date_event,
                start_date_register=form.start_date_register or timezone.now(),
                end_date_register=form.end_date_register,
                description=form.description,
                max_attendee=form.max_attendee,
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return EventResponseSchema.from_orm(event)
    

    @router.get('/events', response=List[EventResponseSchema])
    def list_events(request, status: Optional[str] = None):
        """
        List all events with an optional filter for event status.

        Args:
            status (str, optional): Filter events by status ('upcoming', 'ongoing', 'finished').

        Returns:
            List of events based on the given status.
        """
        now = timezone.now()
        events = Event.objects.all()

        if status == "upcoming":
            events = events.filter(start_date_event__gt=now)
        elif status == "ongoing":
            events = events.filter(start_date_event__lte=now, end_date_event__gte=now)
        elif status == "finished":
            events = events.filter(end_date_event__lt=now)

        return events
    
    @router.get('/my-events', response=List[EventResponseSchema])
    def list_my_events(request):
        """
        List all events created by the authenticated organizer.
        """
        if not request.user.is_authenticated:
            logger.warning(f"Unauthorized access to events list by user: {request.user}")
            return Response({'error': 'User must be logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            organizer = Organizer.objects.get(user=request.user)
            events = Event.objects.filter(organizer=organizer)
            return events
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} attempted to list events but is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=status.HTTP_404_NOT_FOUND)

    # Still can't use.
    @router.put('/edit-event/{event_id}', response={200: dict, 403: dict, 404: dict})
    def edit_event(request, event_id: int, form: EditEventSchema = Form(...)):
        """
        Edit an event's details by event ID.
        Only the organizer who created the event can edit it.
        """
        this_user = request.user
        try:
            organizer = Organizer.objects.get(user=this_user)
        except Organizer.DoesNotExist:
            logger.error(f"User {this_user.username} attempted to edit event {event_id} but is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            event = Event.objects.get(id=event_id, organizer=organizer)
        except Event.DoesNotExist:
            logger.error(f"Organizer {organizer.organizer_name} attempted to edit non-existing event {event_id}.")
            return Response({'error': 'Event does not exist or you do not have permission to edit it'}, status=status.HTTP_404_NOT_FOUND)

        # Update only the fields provided in the form
        if form.event_name is not None:
            event.event_name = form.event_name
        if form.start_date_event is not None:
            event.start_date_event = form.start_date_event
        if form.end_date_event is not None:
            event.end_date_event = form.end_date_event
        if form.start_date_register is not None:
            event.start_date_register = form.start_date_register
        if form.end_date_register is not None:
            event.end_date_register = form.end_date_register
        if form.description is not None:
            event.description = form.description
        if form.max_attendee is not None:
            event.max_attendee = form.max_attendee

        # Save changes to the event
        event.save()

        logger.info(f"Organizer {organizer.organizer_name} edited event {event_id}.")
        return Response({'message': 'Event updated successfully'}, status=status.HTTP_200_OK)
