from .schemas import EventInputSchema, ErrorResponseSchema, EventResponseSchema, FileUploadResponseSchema, EventEngagementSchema, CommentResponseSchema
from .modules import *

router = Router()


class EventAPI:

    @router.post('/create-event', response=EventResponseSchema, auth=JWTAuth())
    def create_event(request, data: EventInputSchema = Form(...), image: UploadedFile = File(None)):
        """
        Create a new event with optional image upload.

        Args:
            request (HttpRequest): The HTTP request object.
            data (EventInputSchema): Event data from the user.
            image (UploadedFile, optional): Image file for the event.

        Returns:
            EventResponseSchema: The created event details or error response.
        """
        this_user = request.user
        try:
            organizer = Organizer.objects.get(user=this_user)
        except Organizer.DoesNotExist:
            raise HttpError(status_code=403, message="You are not an organizer.")
        
        # Create event
        event = Event(**data.dict(), organizer=organizer)
        if not event.is_valid_date():
            return Response({'error': 'Please enter valid date'}, status=400)

        # If an image is provided, upload it
        if image:
            if image.content_type not in ALLOWED_IMAGE_TYPES:
                return Response({'error': 'Invalid file type. Only JPEG and PNG are allowed.'}, status=400)
            
            # (Image upload process, similar to your upload_event_image logic)
            filename = f'event_images/{uuid.uuid4()}{os.path.splitext(image.name)[1]}'
            try:
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                s3_client.upload_fileobj(
                    image.file,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    filename,
                    ExtraArgs={'ContentType': image.content_type}
                )
                event.event_image = filename
                event.save()
                file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{filename}"
                logger.info(f"Uploaded event image for event ID {event.id}: {file_url}")
            except ClientError as e:
                return Response({'error': f"S3 upload failed: {str(e)}"}, status=400)
        
        # Save event and return response
        event.save()
        return EventResponseSchema.from_orm(event)

    @router.get('/my-events', response=List[EventResponseSchema], auth=JWTAuth())
    def get_my_events(request: HttpRequest):
        """
        Retrieve events created by the logged-in organizer.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            List[EventResponseSchema]: List of events created by the organizer.
        """
        try:
            organizer = Organizer.objects.get(user=request.user)
            events = Event.objects.filter(organizer=organizer)
            event_list = []
            for event in events:
                engagement = EventResponseSchema.resolve_engagement(event)
                event_data = EventResponseSchema.from_orm(event)
                event_data.engagement = engagement
                event_list.append(event_data)
            logger.info(f"Organizer {organizer.organizer_name} retrieved their events.")
            return Response(event_list, status=200)
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} tried to access events but is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=404)
        except Exception as e:
            logger.error(f"Error while retrieving events for organizer {request.user.id}: {str(e)}")
            return Response({'error': str(e)}, status=400)

    @router.get('/events', response=List[EventResponseSchema])
    def list_all_events(request: HttpRequest):
        """
        Retrieve all public events for the homepage.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            List[EventResponseSchema]: List of all events.
        """
        try:
            events = Event.objects.filter(event_create_date__lte=timezone.now()).order_by("-event_create_date")
            event_list = []
            for event in events:
                engagement = EventResponseSchema.resolve_engagement(event)
                event_data = EventResponseSchema.from_orm(event)
                event_data.engagement = engagement
                event_list.append(event_data)
            logger.info("Retrieved all events for the homepage.")
            return event_list
        except Exception as e:
            logger.error(f"Error while retrieving events for the homepage: {str(e)}")
            return Response({'error': str(e)}, status=400)

    @router.put('/edit-event-{event_id}', response={204: EventResponseSchema, 401: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def edit_event(request: HttpRequest, event_id: int, data: EventInputSchema):
        """
        Edit an existing event by ID if the user is the organizer.

        Args:
            request (HttpRequest): The HTTP request object.
            event_id (int): ID of the event to edit.
            data (EventInputSchema): Updated event data.

        Returns:
            EventResponseSchema: Updated event details or error response.
        """
        try:
            event = Event.objects.get(id=event_id)
            organizer = Organizer.objects.get(user=request.user)
            if event.organizer != organizer:
                logger.warning(f"User {request.user.username} tried to edit an event they do not own.")
                return Response({'error': 'You are not allowed to edit this event.'}, status=403)
            
            Event.objects.filter(id = event_id).update(**data.dict())
                        
            event_data = EventResponseSchema.from_orm(event).dict()
            logger.info(f"Organizer {organizer.organizer_name} edited their event {event_id}.")
            return Response(event_data, status=204)
        except Event.DoesNotExist:
            logger.error(f"Event with ID {event_id} does not exist.")
            return Response({'error': 'Event not found'}, status=404)
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=404)
        except Exception as e:
            logger.error(f"Error while editing event {event_id}: {str(e)}")
            return Response({'error': str(e)}, status=400)

    @router.get('/{event_id}', response=EventResponseSchema)
    def event_detail(request: HttpRequest, event_id: int):
        """
        Retrieve detailed information for a specific event.

        Args:
            request (HttpRequest): The HTTP request object.
            event_id (int): The ID of the event.

        Returns:
            EventResponseSchema: Details of the specified event.
        """
        logger.info(f"Fetching details for event ID: {event_id} by user {request.user.username}.")
        event = get_object_or_404(Event, id=event_id)
        engagement_data = EventResponseSchema.resolve_engagement(event)
        event_data = EventResponseSchema.from_orm(event)
        event_data.engagement = engagement_data
        return event_data
    
    @router.post('/{event_id}/upload/event-image/', response={200: FileUploadResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())
    def upload_event_image(request: HttpRequest, event_id: int, file: UploadedFile = File(...)):
        """
        Upload an image for a specific event.

        Args:
            request (HttpRequest): The HTTP request object.
            event_id (int): The ID of the event to upload an image for.
            file (UploadedFile): Image file to upload.

        Returns:
            FileUploadResponseSchema: Details of the uploaded image, including URL, or an error response.
        """
        try:
            event = get_object_or_404(Event, id=event_id)

            organizer = Organizer.objects.get(user=request.user)
            if event.organizer != organizer:
                return Response({'error': 'You are not allowed to upload an image for this event.'}, status=403)
            
            if file.content_type not in ALLOWED_IMAGE_TYPES:
                return Response({'error': 'Invalid file type. Only JPEG and PNG are allowed.'}, status=400)
            
            if file.size > MAX_FILE_SIZE:
                return Response({'error': f'File size exceeds the limit of {MAX_FILE_SIZE / (1024 * 1024)} MB.'}, status=400)
            
            # Check if there's an existing image
            if event.event_image:
                old_filename = event.event_image.url
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

            filename = f'event_images/{uuid.uuid4()}{os.path.splitext(file.name)[1]}'
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
                    file.file,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    filename,
                    ExtraArgs={
                        'ContentType': file.content_type,
                    }
                )

                file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{filename}"
                logger.info(f"Successfully uploaded file to S3: {file_url}")
                
                event.event_image = filename
                event.save()
            
                return Response(FileUploadResponseSchema(
                    file_url=file_url,
                    message="Upload successful",
                    file_name=os.path.basename(filename),
                    uploaded_at=timezone.now()
                ), status=200)
            
            except ClientError as e:
                logger.error(f"S3 upload error: {str(e)}")
                return Response({'error': f"S3 upload failed: {str(e)}"}, status=400)
            
        except Organizer.DoesNotExist:
            return Response({'error': 'User is not an organizer'}, status=404)
        except Exception as e:
            return Response({'error': f"Upload failed: {str(e)}"}, status=400)
        
    @router.get('/{event_id}/engagement', response={200: dict})
    def get_event_engagements(request: HttpRequest, event_id: int):
        """
        Retrieve engagement metrics for a specific event.

        Args:
            request (HttpRequest): The HTTP request object, containing user and request metadata.
            event_id (int): The ID of the event for which engagement metrics are requested.

        Returns:
            Response (dict): A dictionary containing engagement metrics for the event.
        """
        event = get_object_or_404(Event, id=event_id)
        engagement_data = EventResponseSchema.resolve_engagement(event)
        return engagement_data                
    
    @router.get('/{event_id}/comments', response=List[CommentResponseSchema])
    def get_events_comments(request: HttpRequest, event_id: int):
        """
        Retrieve all comments for a specific event, including nested replies.
        
        Args:
            request (HttpRequest): The HTTP request object, containing user and request metadata.
            event_id (int): The ID of the event for which comments are requested.

        Returns:
            Response (dict): A dictionary containing comments for the event.
        """
        event = get_object_or_404(Event, id=event_id)
        comments = Comment.objects.filter(event=event, parent=None).select_related('user').prefetch_related('replies', 'reactions').order_by('-created_at')
        response_data = [CommentResponseSchema.from_orm(comment) for comment in comments]
        logger.info(f"Retrieved {len(comments)} comments for event {event_id}.")
        return Response(response_data, status=200)
                