# Standard Library
import json
import logging
import os
import uuid
from abc import ABC, abstractmethod
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

# Third-Party Packages
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from google.auth.transport import requests
from google.oauth2 import id_token
from ninja import File, Form, ModelSchema, Schema
from ninja.errors import HttpError
from ninja.files import UploadedFile
from ninja.responses import Response
from ninja_extra import (
    ControllerBase,
    api_controller,
    route
)
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import AccessToken, RefreshToken
from pydantic import (
    BaseModel, 
    EmailStr, 
    Field, 
    HttpUrl, 
    condecimal, 
    conint, 
    constr,
    field_validator,
)
# Local Modules
from api.models.bookmarks import *
from api.models.comment import *
from api.models.event import *
from api.models.like import *
from api.models.organizer import *
from api.models.ticket import *
from api.models.user import *
from api.utils import *

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg']

