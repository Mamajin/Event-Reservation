from ninja import Router, Schema, NinjaAPI, Field
from django.contrib.auth import authenticate, login
from ninja import NinjaAPI, Router, Schema, ModelSchema, Form
from api.models import *
from rest_framework_simplejwt.tokens import RefreshToken
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


class ErrorResponseSchema(Schema):
    error: str

class OrganizerAPI:
    @router.post('/apply-organizer', response=OrganizerResponseSchema)
    def apply_organizer(request, form: OrganizerSchema = Form(...)):
        """Apply an authenticated user to be an organizer
        
        Return:
            Organizer objects if create successful.
        """
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
        
    @router.delete('/delete-event/{event_id}', response={204: None, 403: ErrorResponseSchema, 404: ErrorResponseSchema})
    def delete_event(request, event_id: int):
        """
        Delete event by event id.
        Only the organizer who created the event can delete it.
        """
        this_user = request.user
        try:
            organizer = Organizer.objects.get(user=this_user)
        except Organizer.DoesNotExist:
            logging.error(f"User {this_user.username} attempted to delete event {event_id} but is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            event = Event.objects.get(id=event_id, organizer=organizer)
            event.delete()
            logging.info(f"Organizer {organizer.organizer_name} deleted event {event_id}.")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            logging.error(f"Organizer {organizer.organizer_name} attempted to delete non-existing event {event_id}.")          
            return Response({'error': 'Event does not exist or you do not have permission to delete it'}, status=status.HTTP_404_NOT_FOUND)
