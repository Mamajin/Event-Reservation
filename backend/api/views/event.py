from ninja import Router, Schema, NinjaAPI, Field
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from ninja import NinjaAPI, Router, Schema, ModelSchema, Form
from typing import List, Optional
from api.models import *
from django.contrib.auth.hashers import make_password
from pydantic import field_validator
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from ninja.responses import Response
from rest_framework import status
from ninja_jwt.authentication import JWTAuth


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
    class Config:
        model = Event
        model_fields = '__all__'



class EventAPI:

    @router.post('/create-event', response=EventResponseSchema, auth= JWTAuth())
    def create_event(request, form: EventSchema = Form(...)):
        this_user = request.user
        try:
            organizer = Organizer.objects.get(user=this_user)
        except Organizer.DoesNotExist:
            return {'error': 
                    'Organizer does not exist.'}, 403

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
            return {'error': str(e)}, 400

        return event
    

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
