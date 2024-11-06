from .schemas import SessionSchema, SessionResponseSchema, ErrorResponseSchema
from .modules import JWTAuth, Organizer, timezone, Event, HttpRequest, logger, Response, Router, Optional, get_object_or_404, Session, datetime, ValidationError

router = Router()


class SessionAPI:

    @router.post('/events/{event_id}/sessions/', response={201: SessionResponseSchema, 400: ErrorResponseSchema, 403: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def create_session(request: HttpRequest, event_id: int, data: SessionSchema):
        """
        Creates a new session for the specified event.

        Parameters:
        - request (HttpRequest): The HTTP request object containing user information.
        - event_id (int): The ID of the event for which the session is being created.
        - data (SessionSchema): The session data to be saved.

        Returns:
        - Response: A response object with status code 201 if session is created successfully,
                    400 if there are validation errors, 403 if user is not an organizer,
                    or 404 if the event is not found.
        """
        try:
            organizer = Organizer.objects.get(user=request.user)
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} attempted to create event({event_id}) session but is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=403)
        
        try:
            event = Event.objects.get(id=event_id, organizer=organizer)
            
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
                end_date_event__gt=data.start_date_event
            ).exists()
            
            if overlapping:
                return Response({
                    'error': 'This session overlaps with an existing session'
                }, status=400)
            session.save()
            return Response(SessionResponseSchema(
                    id=session.id,
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


    @router.delete('/{session_id}/delete/event/{event_id}/', response={204: None, 404: ErrorResponseSchema}, auth=JWTAuth())
    def delete_session(request: HttpRequest, event_id: int, session_id: int):
        """
        Deletes a session for the specified event.

        Parameters:
        - request (HttpRequest): The HTTP request object containing user information.
        - event_id (int): The ID of the event to which the session belongs.
        - session_id (int): The ID of the session to be deleted.

        Returns:
        - Response: A response object with status code 204 if session is deleted successfully,
                    or 404 if the event is not found or user is not authorized to access it.
        """
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
            return Response(status=204)
    
        except Event.DoesNotExist:
            logger.error(f"Event {event_id} not found or user {request.user.username} is not authorized to access it.")
            return Response({"error": "Event not found or you do not have permission to access this event."}, status=404)

    @router.put('/{session_id}/edit/event/{event_id}/', response={200: SessionResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def edit_session(request: HttpRequest, event_id: int, session_id: int, data: SessionSchema):
        """
        Edits an existing session for the specified event.

        Parameters:
        - request (HttpRequest): The HTTP request object containing user information.
        - event_id (int): The ID of the event for which the session is being edited.
        - session_id (int): The ID of the session to be edited.
        - data (SessionSchema): The updated session data.

        Returns:
        - Response: A response object with status code 200 if session is edited successfully,
                    400 if there are validation errors, or 404 if the event is not found.
        """
        try:
            event = Event.objects.get(id=event_id, organizer__user=request.user)
            logger.info(f"Organizer {request.user.username} is attempting to edit session {session_id} for event {event_id}.")
            session = Session.objects.get(id=session_id, event=event)
            
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
                
            session_data = data.dict(exclude_unset=True)
            Session.objects.filter(id=session_id).update(**session_data)
            updated_session = Session.objects.get(id=session_id)
            session_data = SessionResponseSchema.from_orm(updated_session).dict()
            logger.info(f"Session {session_id} updated for event {event_id} by user {request.user.username}")
            return Response(session_data, status=200)
    
        except Event.DoesNotExist:
            logger.error(f"Event {event_id} not found or user {request.user.username} is not authorized to access it.")
            return Response({
                "error": "Event not found or you do not have permission to access this event."
            }, status=404)