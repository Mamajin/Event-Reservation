from .schemas import OrganizerResponseSchema, ErrorResponseSchema,OrganizerSchema
from .modules import HttpRequest, JWTAuth, Form, logger, Response, Organizer, Event, Router, AttendeeUser

router = Router()


class OrganizerAPI:
    @router.post('/apply-organizer',response={201: OrganizerResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())    
    def apply_organizer(request: HttpRequest, form: OrganizerSchema = Form(...)):
        """Apply an authenticated user to be an organizer"""
        try:
            logger.info(f"User {request.user.id} is attempting to apply as an organizer.")
            
            # Validate user isn't already an organizer
            if Organizer.objects.filter(user=request.user).exists():
                logger.info(f"User {request.user.id} already has an organizer profile.")
                return Response({"error": "User is already an organizer"}, status=400)

            # Validate organizer name
            organizer_name = form.organizer_name or ""
            if organizer_name and Organizer.objects.filter(organizer_name=organizer_name).exists():
                logger.info(f"Organizer name '{organizer_name}' is already taken.")
                return Response({"error": "Organizer name is already taken"}, status=400)
                
            # Create and save organizer profile
            organizer = Organizer(
                user=request.user,
                organizer_name=organizer_name,
                email=form.email or request.user.email,
                organization_type=form.organization_type,
            )
            
            # Validate the model
            organizer.full_clean()
            organizer.save()
            
            request.user.status = "Organizer"
            request.user.save()
            
            
            logger.info(f"User {request.user.id} successfully applied as an organizer with ID {organizer.id}.")
            
            # Return formatted response
            return Response(OrganizerResponseSchema.from_orm(organizer), status=201)
        
        except Exception as e:
            logger.error(f"Unexpected error while creating organizer for user {request.user.id}: {str(e)}")
            return 400, {"error": "An unexpected error occurred"}

    @router.delete('/delete-event/{event_id}', response={204: None, 403: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def delete_event(request: HttpRequest, event_id: int):
        """Delete event by event id."""
        try:
            organizer = Organizer.objects.get(user=request.user)
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} attempted to delete event {event_id} but is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=403)
        
        try:
            event = Event.objects.get(id=event_id, organizer=organizer)
            event.delete()
            logger.info(f"Organizer {organizer.organizer_name} deleted event {event_id}.")
            return Response({'success': f" Delete event ID {event_id} successfully"},status=204)
        except Event.DoesNotExist:
            logger.error(f"Organizer {organizer.organizer_name} attempted to delete non-existing event {event_id}.")
            return Response({'error': 'Event does not exist or you do not have permission to delete it'}, status=404)

    @router.put('/update-organizer', response={200: OrganizerResponseSchema, 401: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def update_organizer(request: HttpRequest, data: OrganizerSchema):
        """Update the profile information of the authenticated organizer."""
        
        organizer = Organizer.objects.get(user=request.user)
        organizer.organizer_name = data.organizer_name
        organizer.email = data.email
        organizer.organization_type = data.organization_type
        
        if organizer.organizer_name_is_taken(data.organizer_name):
            logger.info(f"Organizer name '{data.organizer_name}' is already taken.")
            return Response({'error': 'Organizer name is already taken'}, status=400)
        
        organizer.save()

        logger.info(f"User {request.user.id} updated their organizer profile.")
        
        return Response(
            OrganizerResponseSchema(
                id=organizer.id,
                organizer_name=organizer.organizer_name,
                email=organizer.email,
                organization_type=organizer.organization_type,
                is_verified=organizer.is_verified,
            ).dict(),
            status=200
        )
            
    @router.delete('/revoke-organizer', response={204: None, 403: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def revoke_organizer(request: HttpRequest):
        """Revoke the organizer role of the authenticated user."""
        try:
            organizer = Organizer.objects.get(user=request.user)
            organizer.delete()
            logger.info(f"Organizer role revoked for user {request.user.id}.")
            return Response({'success':f'Organizer role revoked for user {request.user.id}.'},status=204)
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} tried to revoke a non-existing organizer profile.")
            return Response({'error': 'User is not an organizer'}, status=404)
        
    @router.get('/view-organizer', response={200: OrganizerResponseSchema, 401: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def view_organizer(request: HttpRequest):
        """View the organizer profile."""
        try:
            organizer = Organizer.objects.get(user=request.user)
            logger.info(f"User {request.user.id} viewed their organizer profile.")
            return OrganizerResponseSchema(
                id=organizer.id,
                organizer_name=organizer.organizer_name,
                email=organizer.email,
                organization_type=organizer.organization_type,
                is_verified=organizer.is_verified
            )
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} tried to access a non-existing organizer profile.")
            return Response({'error': 'User is not an organizer'}, status=404)
