from .schemas import SessionSchema, SessionResponseSchema, ErrorResponseSchema
from .modules import JWTAuth, Organizer, timezone, Event, HttpRequest, logger, Response, Router, Optional, get_object_or_404, Session, datetime

router = Router()


class SessionAPI:

    @router.post('/events/{event_id}/sessions', response={201: SessionResponseSchema, 400: ErrorResponseSchema, 403: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def create_session(request: HttpRequest, event_id: int, data: SessionSchema):
        if not request.user.is_authenticated:
            logger.warning(f"Unauthorized access to create or assign session by user: {request.user}")
            return Response({'error': 'User must be logged in'}, status=401)

        try:
            organizer = Organizer.objects.get(user=request.user)
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} attempted to create event({event_id}) session but is not an organizer.")
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

    @router.delete('/{session_id}/delete/event/{event_id}', response={204: None, 404: ErrorResponseSchema}, auth=JWTAuth())
    def delete_session(request: HttpRequest, event_id: int, session_id: int):
        try:
            event = Event.objects.get(id=event_id, organizer__user=request.user)
            logger.info(f"Organizer {request.user.username} is attempting to delete session {session_id} for event {event_id}.")
            
            session = get_object_or_404(Session, id=session_id, event=event)
            
            session.delete()
            logger.info(f"Session {session_id} for event {event_id} deleted by user {request.user.username}.")
            return Response(status=204)
    
        except Event.DoesNotExist:
            logger.error(f"Event {event_id} not found or user {request.user.username} is not authorized to access it.")
            return Response({"error": "Event not found or you do not have permission to access this event."}, status=404)

    @router.put('/{session_id}/edit/event/{event_id}', response={200: SessionResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def edit_session(request: HttpRequest, event_id: int, session_id: int, data: SessionSchema):
        try:
            event = Event.objects.get(id=event_id, organizer__user=request.user)
            logger.info(f"Organizer {request.user.username} is attempting to edit session {session_id} for event {event_id}.")
            
            session = get_object_or_404(Session, id=session_id, event=event)

            session.session_name = data.session_name
            session.start_date_event = data.start_date_event
            session.end_date_event = data.end_date_event
            session.start_date_register = data.start_date_register or timezone.now()
            session.end_date_register = data.end_date_register
            session.description = data.description
            session.max_attendee = data.max_attendee
            session.session_type = data.session_type
            session.save()
            
            logger.info(f"Organizer {request.user.username} updated their session({session_id}) detail from event({event_id}).")
            
            return Response(
                SessionResponseSchema.from_orm(session),
                status=200
            )
    
        except Event.DoesNotExist:
            logger.error(f"Event {event_id} not found or user {request.user.username} is not authorized to access it.")
            return Response({"error": "Event not found or you do not have permission to access this event."}, status=404)
        