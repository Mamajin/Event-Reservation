from .schemas import SessionSchema, SessionResponseSchema, ErrorResponseSchema
from .modules import JWTAuth, Organizer, timezone, Event, HttpRequest, logger, Response, Router, Optional, get_object_or_404, Session, datetime, ValidationError

router = Router()


class SessionAPI:

    @router.post('/events/{event_id}/sessions', response={201: SessionResponseSchema, 400: ErrorResponseSchema, 403: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def create_session(request: HttpRequest, event_id: int, data: SessionSchema):
        try:
            organizer = Organizer.objects.get(user=request.user)
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} attempted to create event({event_id}) session but is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=403)
        
        try:
            event = get_object_or_404(Event, id=event_id)
            
            session = Session(
                event=event,
                session_name=data.session_name,
                session_type=data.session_type,
                start_date_event=data.start_date_event,
                end_date_event=data.end_date_event,
                start_date_register=data.start_date_register or timezone.now(),
                end_date_register=data.end_date_register,
                description=data.description,
                max_attendee=data.max_attendee
            )

            if data.start_date_event < event.start_date_event or data.end_date_event > event.end_date_event:
                return Response({
                    'error': 'Session dates must be within event dates'
                }, status=400)

            # Check for overlapping sessions
            overlapping = Session.objects.filter(
                event=event,
                start_date_event__lt=data.end_date_event,
                end_date_event__gt=data.start_date_event,
                session_type=session.session_type
            ).exists()
            
            if overlapping:
                return Response({
                    'error': 'This session overlaps with an existing session'
                }, status=400)
            session.save()
            return Response(SessionResponseSchema(
                    **session.get_session_detail()
                ), status=201)
        except Event.DoesNotExist:
            logger.error(f"Event with ID {event_id} does not exist or access denied.")
            return Response({'error': 'Event not found or access denied'}, status=404)
        except ValidationError as e:
            logger.error(f"Validation error while creating session for event {event_id}: {str(e)}")
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            logger.error(f"Error while creating session for event {event_id}: {str(e)}")
            return Response({'error': str(e)}, status=400)


    @router.delete('/{session_id}/delete/event/{event_id}', response={204: None, 404: ErrorResponseSchema}, auth=JWTAuth())
    def delete_session(request: HttpRequest, event_id: int, session_id: int):
        try:
            event = Event.objects.get(id=event_id, organizer__user=request.user)
            logger.info(f"Organizer {request.user.username} is attempting to delete session {session_id} for event {event_id}.")
            session = get_object_or_404(Session, id=session_id, event=event)
            
            if session.is_active:
                return Response({
                    'error': 'Cannot delete an active session'
                }, status=400)
            
            session.delete()
            logger.info(f"Session {session_id} for event {event_id} deleted by user {request.user.username}.")
            return Response({'success': f'Session {session_id} for event {event_id} is deleted.'}, status=204)
    
        except Event.DoesNotExist:
            logger.error(f"Event {event_id} not found or user {request.user.username} is not authorized to access it.")
            return Response({"error": "Event not found or you do not have permission to access this event."}, status=404)

    @router.put('/{session_id}/edit/event/{event_id}', response={200: SessionResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def edit_session(request: HttpRequest, event_id: int, session_id: int, data: SessionSchema):
        try:
            event = Event.objects.get(id=event_id, organizer__user=request.user)
            logger.info(f"Organizer {request.user.username} is attempting to edit session {session_id} for event {event_id}.")
            
            session = get_object_or_404(Session, id=session_id, event=event)
            
            if session.is_active or timezone.now() > session.end_date_event:
                return Response({
                    'error': 'Cannot edit active or completed sessions'
                }, status=400)

            # Check for overlapping sessions excluding current session
            overlapping = Session.objects.filter(
                event=event,
                start_date_event__lt=data.end_date_event,
                end_date_event__gt=data.start_date_event
            ).exclude(id=session_id).exists()
            
            if overlapping:
                return Response({
                    'error': 'This session would overlap with an existing session'
                }, status=400)
                
            session.session_name = data.session_name
            session.session_type = data.session_type
            session.start_date_event = data.start_date_event
            session.end_date_event = data.end_date_event
            session.start_date_register = data.start_date_register or timezone.now()
            session.end_date_register = data.end_date_register
            session.description = data.description
            session.max_attendee = data.max_attendee
            session.save()
            
            logger.info(f"Organizer {request.user.username} updated their session({session_id}) detail from event({event_id}).")
            
            try:
                session.save()
            except ValidationError as e:
                return Response({'error': str(e)}, status=400)
            
            logger.info(f"Session {session_id} updated for event {event_id} by user {request.user.username}")
            return Response(SessionResponseSchema.from_orm(session), status=200)
    
        except Event.DoesNotExist:
            logger.error(f"Event {event_id} not found or user {request.user.username} is not authorized to access it.")
            return Response({
                "error": "Event not found or you do not have permission to access this event."
            }, status=404)
            
    @router.get('/{session_id}/details', response=SessionResponseSchema)
    def session_detail(request: HttpRequest, session_id: int):
        """
        Get Session deatils by session id
        """
        logger.info('User view session details.')
        session = get_object_or_404(Session, id=session_id)
        return Response(SessionResponseSchema.from_orm(session).dict(), status=200)
    