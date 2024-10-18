from ninja import Router, Schema, NinjaAPI, Field
from django.contrib.auth import authenticate, login
from ninja import NinjaAPI, Router, Schema, ModelSchema, Form
from typing import Optional
from ninja.security import django_auth
from api.models import *
from ninja.errors import HttpError
from django.http import HttpRequest
from ninja.responses import Response
from rest_framework import status
import logging


logger = logging.getLogger(__name__)
router = Router()


class OrganizerSchema(Schema):
    organizer_name: Optional[str]
    email: Optional[str]


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
        
    @router.get('/organizer-profile', response=OrganizerResponseSchema, auth=django_auth)
    def view_organizer_profile(request):
        """
        Get the profile of the currently authenticated organizer.
        """
        if not request.user.is_authenticated:
            logger.warning(f"Unauthorized access to organizer profile by user: {request.user}")
            return Response({'error': 'User must be logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            organizer = Organizer.objects.get(user=request.user)
            return OrganizerResponseSchema(
                id=organizer.id,
                organizer_name=organizer.organizer_name,
                email=organizer.email
            )
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} tried to access an organizer profile but is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=status.HTTP_404_NOT_FOUND)

    # Still can't use.
    @router.put('/update-organizer', response={200: OrganizerResponseSchema, 401: ErrorResponseSchema, 404: ErrorResponseSchema})
    def update_organizer(request: HttpRequest, form: OrganizerSchema):
        """
        Update the profile information of the authenticated organizer.
        """
        if not request.user.is_authenticated:
            logger.warning(f"Unauthorized organizer update attempt by user: {request.user}")
            return Response({'error': 'User must be logged in to update organizer profile'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            organizer = Organizer.objects.get(user=request.user)
            
            # Update only the fields provided in the form
            if form.organizer_name is not None:
                organizer.organizer_name = form.organizer_name
            else:
                organizer.organizer_name = organizer.organizer_name
            if form.email is not None:
                organizer.email = form.email
            else:
                organizer.email = organizer.email
            
            organizer.save()
            logger.info(f"User {request.user.id} updated their organizer profile.")
            
            return Response(OrganizerResponseSchema(
                id=organizer.id,
                organizer_name=organizer.organizer_name,
                email=organizer.email
            ).dict())
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} tried to update an organizer profile but is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error while updating organizer for user {request.user.id}: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
@router.delete('/revoke-organizer', response={204: None, 403: ErrorResponseSchema, 404: ErrorResponseSchema})
def revoke_organizer(request):
    """
    Revoke the organizer role of the authenticated user.
    """
    if not request.user.is_authenticated:
        logger.warning(f"Unauthorized revocation attempt by user: {request.user}")
        return Response({'error': 'User must be logged in'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        organizer = Organizer.objects.get(user=request.user)
        organizer.delete()
        logger.info(f"Organizer role revoked for user {request.user.id}.")
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Organizer.DoesNotExist:
        logger.error(f"User {request.user.username} tried to revoke a non-existing organizer profile.")
        return Response({'error': 'User is not an organizer'}, status=status.HTTP_404_NOT_FOUND)

