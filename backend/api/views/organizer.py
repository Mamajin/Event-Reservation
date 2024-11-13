from .schemas import OrganizerResponseSchema, ErrorResponseSchema, OrganizerSchema, FileUploadResponseSchema, OrganizerUpdateSchema
from .modules import *

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

    @router.patch('/update-organizer', response={200: OrganizerUpdateSchema, 401: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def update_organizer(request: HttpRequest, data: OrganizerUpdateSchema):
        """Update the profile information of the authenticated organizer."""

        organizer = Organizer.objects.get(user=request.user)

        # Check if organizer_name is being updated and if the new name is already taken
        if data.organizer_name != organizer.organizer_name and organizer.organizer_name_is_taken(data.organizer_name):
            logger.info(f"Organizer name '{data.organizer_name}' is already taken.")
            return Response({'error': 'Organizer name is already taken'}, status=400)
        
        
        update_fields = data.dict(exclude_unset = True)
        for field, value in update_fields.items():
            setattr(organizer, field, value)
            
        organizer.save()
    
        organize_data = OrganizerUpdateSchema.from_orm(organizer).dict()

        logger.info(f"User {request.user.id} updated their organizer profile.")
        
        return Response(organize_data, status=200)
            
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
        organizer = get_object_or_404(Organizer, user=request.user)
        logger.info(f"User {request.user.id} viewed their organizer profile.")
        organizer_dict = OrganizerResponseSchema.from_orm(organizer).dict()
        return Response(OrganizerResponseSchema(**organizer_dict), status=200)
        
    @router.post('/{organizer_id}/upload/logo/', response={200: FileUploadResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())
    def upload_profile_picture(request: HttpRequest, organizer_id: int, logo: UploadedFile = File(...)):
        """
        Upload a logo for a organzier's profile.
        """
        try:
            organizer = get_object_or_404(Organizer, id=organizer_id)
            
            if logo.content_type not in ALLOWED_IMAGE_TYPES:
                return Response({'error': 'Invalid file type. Only JPEG and PNG are allowed.'}, status=400)
            
            if logo.size > MAX_FILE_SIZE:
                return Response({'error': f'File size exceeds the limit of {MAX_FILE_SIZE / (1024 * 1024)} MB.'}, status=400)
            
            # Check if there's an existing image
            if organizer.logo:
                old_filename = organizer.logo.url
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                try:
                    s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=old_filename)
                    logger.info(f"Deleted old image from S3: {old_filename}")
                except ClientError as e:
                    logger.error(f"Failed to delete old image from S3: {str(e)}")

            filename = f'logos/{uuid.uuid4()}{os.path.splitext(logo.name)[1]}'
            logger.info(f"Starting upload for file: {filename}")
            try:
                # Direct S3 upload using boto3
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )

                # Upload file to S3
                s3_client.upload_fileobj(
                    logo.file,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    filename,
                    ExtraArgs={
                        'ContentType': logo.content_type,
                    }
                )

                file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{filename}"
                logger.info(f"Successfully uploaded file to S3: {file_url}")
                
                organizer.logo = filename
                organizer.save()
            
                return Response(FileUploadResponseSchema(
                    file_url=file_url,
                    message="Upload successful",
                    file_name=os.path.basename(filename),
                    uploaded_at=timezone.now()
                ), status=200)
            
            except ClientError as e:
                logger.error(f"S3 upload error: {str(e)}")
                return Response({'error': f"S3 upload failed: {str(e)}"}, status=400)
            
        except Exception as e:
            return Response({'error': f"Upload failed: {str(e)}"}, status=400)
                    
