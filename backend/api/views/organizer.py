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


router = Router()



class OrganizerSchema(ModelSchema):
    class Config:
        model = Organizer
        model_fields = '__all__'


class OrganizerResponseSchema(Schema):
    organizer_name: str