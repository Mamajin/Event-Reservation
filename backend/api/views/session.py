from ninja import Router, Schema
from ninja import Router, Schema, Form
from ninja.responses import Response
from ninja_jwt.authentication import JWTAuth
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from typing import List, Optional
from api.models import *
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = Router()


class SessionSchema(Schema):
    session_name: str
    start_date_event: datetime
    end_date_event: datetime
    start_date_register: Optional[datetime]
    end_date_register: datetime
    description: str
    max_attendee: int
    session_type: str


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
    session_type: str


class ErrorResponseSchema(Schema):
    error: str


class SessionAPI:

    @router.post('/events/{event_id}', response={201: SessionResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())
    def create_session(request: HttpRequest, event_id: int, data: SessionSchema):
        """Create a new session for an event."""
        if not request.user.is_authenticated:
            logger.warning(f"Unauthorized access to create or assign session by user: {request.user}")
            return Response({'error': 'User must be logged in'}, status=401)

        try:
            organizer = Organizer.objects.get(user=request.user)
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} attempted to delete event {event_id} but is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=403)
        
        try:
            event = Event.objects.get(id=event_id, organizer=organizer)

            if event.organizer != organizer:
                logger.warning(f"User {request.user.username} tried to create a session for an event they do not own.")
                return Response({'error': 'You are not allowed to add sessions to this event.'}, status=403)
            
            session = Session.objects.create(
                event=event,
                session_name=data.session_name,
                start_date_event=data.start_date_event,
                end_date_event=data.end_date_event,
                start_date_register=data.start_date_register or timezone.now(),
                end_date_register=data.end_date_register,
                description=data.description,
                max_attendee=data.max_attendee,
                session_type=data.session_type
            )
            return Response(SessionResponseSchema.from_orm(session), status=201)
        except Event.DoesNotExist:
            logger.error(f"Event with ID {event_id} does not exist or access denied.")
            return Response({'error': 'Event not found or access denied'}, status=404)
        except Exception as e:
            logger.error(f"Error while creating session for event {event_id}: {str(e)}")
            return Response({'error': str(e)}, status=400)
        
    @router.delete('/{event_id}/delete-session/{session_id}', response={204: None, 404: ErrorResponseSchema}, auth=JWTAuth())
    def delete_session(request: HttpRequest, event_id: int, session_id: int):
        """Delete a session by session id from event id."""
        session = get_object_or_404(Session, 
                                    id=session_id, 
                                    event__organizer__user=request.user,
                                    event__id=event_id)
        session.delete()
        logger.info(f"Session {session_id} for event {event_id} deleted by user {request.user.username}.")
        return Response(status=204)
