from ninja import Router, Schema
from ninja import Router, Schema, ModelSchema, Form
from typing import List, Optional
from api.models import *
from datetime import datetime
from ninja.responses import Response
from ninja_jwt.authentication import JWTAuth

router = Router()

class SessionSchema(ModelSchema):
    class Meta:
        model = Session
        fields = ['session_name', 'start_time', 'end_time', 'description', 'max_participants']

class SessionResponseSchema(Schema):
    id: int
    session_name: str
    event_create_date: datetime
    start_date_event: datetime
    end_date_event: datetime
    start_date_register: datetime
    end_date_register: datetime
    description: str
    max_attendee: int
