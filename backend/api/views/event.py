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
from ninja.security import django_auth
from ninja.errors import HttpError


router = Router()


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['id', 'username', 'password','email'] 
        
 
class OrganizerSchema(ModelSchema):
    user : UserSchema
    
    class Meta:
        model = Organizer
        fields = ['user', 'organizer_name', 'email']


class EventSchema(ModelSchema):
    organizer: OrganizerSchema
    class Meta:
        model = Event
        fields = [
            'event_name',
            'organizer',
            'event_create_date',
            'start_date_event',
            'end_date_event',
            'start_date_register',
            'end_date_register',
            'description',
            'max_attendee',
        ]
        

class EventAPI:

    @router.post('/create-event', response=EventSchema)
    def create_event(request, data: EventSchema):
        this_user = request.user
        
        # Ensure the user is authenticated
        if not this_user.is_authenticated:
            raise HttpError(status_code=403, message="You must be logged in to create an event.")
        
        try:
            # Get the organizer associated with the current user
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