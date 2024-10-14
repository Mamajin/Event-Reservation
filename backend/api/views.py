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


api = NinjaAPI(version ="2.0.0")
router = Router()


api.add_router("", router)


class UserSchema(Schema):
    username: str
    password: str
    password2: str
    
    @field_validator("password2")
    def passwords_match(cls, password2, values, **kwargs):
        if "password" in values.data and values.data["password"] != password2:
            raise ValueError("Passwords do not match")
        return password2
    
class LoginSchema(Schema):
    username: str
    password: str

class UserResponseSchema(Schema):
    username: str
    access_token: str
    refresh_token: str


class OrganizerSchema(ModelSchema):
    class Config:
        model = Organizer
        model_fields = '__all__'


class OrganizerResponseSchema(Schema):
    organizer_name: str


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


class AttendeeSchema(ModelSchema):
    class Config:
        model = Attendee
        model_fields = '__all__'


class TicketSchema(ModelSchema):
    class Config:
        model = Ticket
        model_fields = '__all__'


class UserAPI:
            
    @router.post('/register', response=UserResponseSchema)
    def create_user(request, form: UserSchema = Form(...)):
        if form.password != form.password2:
            return {"error": "Passwords do not match"}
        if User.objects.filter(username = form.username).exists():
            return {"error": "Username already taken"}
        user = User.objects.create(username = form.username, password =make_password(form.password))
        refresh = RefreshToken.for_user(user)
        return {"username":user.username, "access_token": str(refresh.access_token), "refresh_token": str(refresh)}
    
    
    
    @router.post('/login', response = LoginSchema)
    def login(request, form: LoginSchema = Form(...)):
        user = authenticate(request, username = form.username, password = form.password)
            
        if user is not None:
            login(request,user)
            return {"success": True, "message": "Login successful", "username": user.username, "password": user.password}
        else:
            return Response(
            {"success": False, "message": "Invalid username or password"},
            status=status.HTTP_403_FORBIDDEN
        )
        
    
    

class EventAPI:

    @router.post('/create-event', response=EventResponseSchema)
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
