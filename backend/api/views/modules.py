from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from ninja import Schema, ModelSchema, Form, Router, File
from ninja.responses import Response
from ninja.errors import HttpError
from ninja.files import UploadedFile
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import AccessToken, RefreshToken
from api.utils import *
from api.models.user import *
from api.models.event import *
from api.models.bookmarks import *
from api.models.like import *
from api.models.organizer import *
from api.models.ticket import *
from api.models.session import *
from api.models.comment import *
from botocore.exceptions import ClientError
from pydantic import EmailStr, HttpUrl, constr, conint, Field
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal
from enum import Enum
from google.oauth2 import id_token
from google.auth.transport import requests
import logging
import os
import uuid
import boto3

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg']
