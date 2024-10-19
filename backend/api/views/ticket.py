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
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth

router = Router()


class TicketSchema(ModelSchema):
    class Meta:
        model = Ticket
        fields = ['event', 'attendee', 'register_date']

class TicketAPI:
    @router.get('event/{user_id}', response=List[TicketSchema], auth = JWTAuth())
    def list_event(request, user_id: int):
        user = get_object_or_404(AttendeeUser, id = user_id)
        return user.ticket_set.all()
        