from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from ninja import Schema, ModelSchema, Form, Router, File
from ninja.responses import Response
from ninja.errors import HttpError
from ninja.files import UploadedFile
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import AccessToken, RefreshToken
from api.models.user import *
from api.models.event import *
from api.models.organizer import *
from api.models.ticket import *
from api.models.session import *
from pydantic import EmailStr, HttpUrl, constr, conint, Field
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal
from enum import Enum
import logging

logger = logging.getLogger(__name__)
