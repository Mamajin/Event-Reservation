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
import logging


logger = logging.getLogger(__name__)
router = Router()


class OrganizerSchema(Schema):
    organizer_name: str
    email: str


class OrganizerResponseSchema(Schema):
    id: int
    organizer_name: str
    email: str


class OrganizerAPI:
    @router.post('/apply-organizer', response=OrganizerResponseSchema)
    def apply_organizer(request, form: OrganizerSchema = Form(...)):
        if not request.user.is_authenticated:
            logger.warning(f"Unauthorized organizer application attempt by user: {request.user}")
            return Response({'error': 'User must be logged in to apply as an organizer'}, status=status.HTTP_401_UNAUTHORIZED)

        logger.info(f"User {request.user.id} is attempting to apply as an organizer.")

        if Organizer.objects.filter(user=request.user).exists():
            logger.info(f"User {request.user.id} already has an organizer profile.")
            return Response({'error': 'User is already an organizer'}, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            organizer = Organizer.objects.create(
                user=request.user,
                organizer_name=form.organizer_name,
                email=form.email
            )
            logger.info(f"User {request.user.id} successfully applied as an organizer with ID {organizer.id}.")
            
            return Response({
            'id': organizer.id,
            'organizer_name': organizer.organizer_name,
            'email': organizer.email
        }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error while creating organizer for user {request.user.id}: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
