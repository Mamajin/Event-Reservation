from ninja import Router, Schema, NinjaAPI, Field
from django.contrib.auth.models import User
from ninja import NinjaAPI, Router, Schema, ModelSchema, Form
from typing import List, Optional
from api.models import *
from django.contrib.auth.hashers import make_password
from pydantic import field_validator
from rest_framework_simplejwt.tokens import RefreshToken
import datetime


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
        
    # @validator("end_date_event")
    # def check_end_date_event(cls, end_date_event, values):
    #     if "start_date_event" in values and datetime.fromisoformat(end_date_event) < datetime.fromisoformat(values["start_date_event"]):
    #         raise ValueError("End date of the event must be after the start date.")
    #     return end_date_event
    

    # @validator("end_date_register")
    # def check_end_date_register(cls, end_date_register, values):
    #     if "start_date_event" in values and datetime.fromisoformat(end_date_register) > datetime.fromisoformat(values["start_date_event"]):
    #         raise ValueError("End date of registration must be before the event start date.")
    #     return end_date_register


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
