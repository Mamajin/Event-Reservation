from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from ninja import Schema, ModelSchema, Form, Router
from typing import List, Optional
from api.models.attendeeuser import *
from api.models.event import *
from api.models.organizer import *
from api.models.ticket import *
from api.models.session import *
from django.contrib.auth.hashers import make_password
from pydantic import field_validator
from datetime import datetime, date
from ninja.responses import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import AccessToken, RefreshToken
from django.http import HttpRequest
from ninja.errors import HttpError
import logging

logger = logging.getLogger(__name__)
