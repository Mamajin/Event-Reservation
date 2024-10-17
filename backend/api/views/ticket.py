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


router = Router()


class TicketSchema(ModelSchema):
    class Config:
        model = Ticket
        model_fields = '__all__'
        
class TicketResponseSchema(Schema):
    register_id : int
    event : str
    attendee: str
    date : datetime
    

@router.post("/events/{event_id}/enroll", response= TicketSchema)
def enroll_event(request, event_id):
    user = request.user
    if not user.is_authenticated:
        return {"error": "You must be logged in to enroll in an event."}
    event = get_object_or_404(Event , id = event_id)
    ticket = Ticket.objects.create(event = event , attendee = user)
    return ticket