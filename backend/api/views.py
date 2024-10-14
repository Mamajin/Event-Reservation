from ninja import Router, Schema, NinjaAPI, Field
from django.contrib.auth.models import User
from ninja import NinjaAPI, Router, Schema, ModelSchema, Form
from typing import List
from api.models import *
from django.contrib.auth.hashers import make_password
from pydantic import field_validator
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken



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

class EventSchema(ModelSchema):
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
            
    @router.post('/register', response = UserResponseSchema)
    def create_user(request, form : UserSchema = Form(...)):
        if form.password != form.password2:
            return {"error": "Passwords do not match"}
        if User.objects.filter(username = form.username).exists():
            return {"error": "Username already taken"}
        user = User.objects.create(username = form.username, password =make_password(form.password))
        refresh = RefreshToken.for_user(user)
        return {"username":user.username, "access_token": str(refresh.access_token), "refresh_token": str(refresh)}
    
