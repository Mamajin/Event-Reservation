from abc import ABC, abstractmethod
from api.views.modules import *
from api.views.schemas.event_schema import *
from api.views.schemas.other_schema import *
from api.views.schemas.comment_schema import CommentResponseSchema
from api.views.schemas.user_schema import UserResponseSchema
from api.views.schemas.ticket_schema import TicketResponseSchema


class EventStrategy(ABC):
    """
    Base class for event strategies.
    """

    def __init__(self, request: HttpRequest):
        self.user = request.user
        self.request = request

    @staticmethod
    def get_strategy(strategy_name : str, request : HttpRequest):
        """
        Retrieve the event strategy instance based on the provided strategy name.

        Args:
            strategy_name (str): The name of the strategy to retrieve.
            request (HttpRequest): The HTTP request object, containing user and request metadata.

        Returns:
            An instance of the strategy corresponding to the given strategy name,
            or None if the strategy name is not recognized.
        """
        strategies = {
            'create_event': EventCreateStrategy(request),
            'organizer_get_events': EventOrganizerStrategy(request),
            'list_event': EventListStrategy(request),
            'event_detail': EventDetailStrategy(request),
            'edit_event': EventEditStrategy(request),
            'upload_event_image': EventUploadImageStrategy(request),
        }
        return strategies.get(strategy_name)
    
    @abstractmethod
    def execute(self, *arg, **kwargs):
        """
        Execute the event strategy with the given arguments.

        Args:
            *arg: Variable length argument list. The arguments passed to this method
                depend on the specific strategy being executed.
            **kwargs: Keyword argument dictionary. The keyword arguments passed to this
                method depend on the specific strategy being executed.

        Raises:
            NotImplementedError: If the execute method is not implemented in the derived class.
        """

        pass
    
    def upload_image(self,image,event):
        """
        Upload an image for an event.

        Args:
            image (InMemoryUploadedFile): The image file to upload.
            event (Event): The event for which to upload the image.

        Returns:
            Response: A response containing the uploaded image URL, or an error response if the
                upload fails.
        """

        if image.content_type not in ALLOWED_IMAGE_TYPES:
                return Response({'error': 'Invalid file type. Only JPEG and PNG are allowed.'}, status=400)
            
            # (Image upload process, similar to your upload_event_image logic)
        filename = f'event_images/{uuid.uuid4()}{os.path.splitext(image.name)[1]}'
        try:
            self.upload_s3(image, filename)
            event.event_image = filename
            event.save()
            file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{filename}"
            logger.info(f"Uploaded event image for event ID {event.id}: {file_url}")
        except ClientError as e:
            return Response({'error': f"S3 upload failed"}, status=400)
        event.save()
        return EventResponseSchema.from_orm(event)

    def upload_s3(self, image, filename):
        """
        Upload an image file to an S3 bucket.

        Args:
            image (InMemoryUploadedFile): The image file to be uploaded.
            filename (str): The target filename for the uploaded image in the S3 bucket.

        Returns:
            None
        """
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
    
    def add_event(self, event_list: list, events : list):
        """
        Add event data to a list, including engagement information and user engagement status.

        Args:
            event_list (list): The list to which event data will be added.
            events (QuerySet): The events for which data will be added to the list.
        """
        for event in events:
                engagement = EventResponseSchema.resolve_engagement(event)
                user_engaged = EventResponseSchema.resolve_user_engagement(event, self.user)
                EventResponseSchema.set_status_event(event)
                event_data = EventResponseSchema.from_orm(event)
                event_data.engagement = engagement
                event_data.user_engaged = user_engaged
                event_list.append(event_data)
                
                
    def autheticate_user(self):
        """
        Authenticate the user using a JWT token in the Authorization header, or else use the
        user from the request object.

        Args:
            None

        Returns:
            None
        """
        if self.request.headers.get("Authorization"):
            token = self.request.headers.get('Authorization')
            if token != None and token.startswith('Bearer '):
                token = token[7:]
                if JWTAuth().authenticate(self.request,token):
                    user = JWTAuth().authenticate(self.request, token)
                    self.user = user
        else:
            self.user = self.request.user
        
    
    
class EventCreateStrategy(EventStrategy):
    """
    Strategy for creating an event.
    """
            
    def execute(self, data: EventInputSchema = Form(...), image : UploadedFile = File(None)):
        """
        Create an event with the given data and optional image file.

        Args:
            data (EventInputSchema): The event data, passed as a form.
            image (UploadedFile, optional): The image file for the event, passed as a file.

        Returns:
            Response: The created event object, or an error response if the creation fails.
        """
        try:
            organizer = Organizer.objects.get(user=self.user)
        except Organizer.DoesNotExist:
            raise HttpError(status_code=403, message="You are not an organizer.")
        
        # Create event
        event = Event(**data.dict(), organizer=organizer)
        if not event.is_valid_date():
            return Response({'error': 'Please enter valid date'}, status=400)
        if image:
            return self.upload_image(image, event)
        event.save()
        return EventResponseSchema.from_orm(event)
    
class EventOrganizerStrategy(EventStrategy):
    """
    Strategy for retrieving events for an organizer.
    """
        
    def execute(self):
        """
        Retrieve events created by the authenticated organizer.

        Args:
            None

        Returns:
            Response: List of events created by the organizer, ordered by event creation date in descending order.
            ErrorResponseSchema: Error message with status code 404 if the user is not an organizer,
            or 400 in case of other errors.
        """
        try:
            organizer = Organizer.objects.get(user=self.user)
            events = Event.objects.filter(organizer=organizer, event_create_date__lte=timezone.now()).order_by("-event_create_date")
            event_list = []
            self.add_event(event_list,events)
            logger.info(f"Organizer {organizer.organizer_name} retrieved their events.")
            return Response(event_list, status=200)
        except Organizer.DoesNotExist:
            logger.error(f"User {self.user.username} tried to access events but is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=404)
        except Exception as e:
            logger.error(f"Error while retrieving events for organizer {self.user.id}: {str(e)}")
            return Response({'error': str(e)}, status=400)
    
    
class EventListStrategy(EventStrategy):
    """
    Strategy for retrieving all public events.
    """
    def execute(self):
        """
        Retrieve all public events for the homepage.

        Args:
            None

        Returns:
            Response: List of all public events, ordered by event creation date in descending order.
            ErrorResponseSchema: Error message with status code 400 in case of other errors.
        """
        events = Event.objects.filter(event_create_date__lte=timezone.now()).order_by("-event_create_date")
        event_list = []
        self.autheticate_user()

        self.add_event(event_list,events)

        # Conditionally add user-specific engagement data

        logger.info("Retrieved all public events for the homepage.")
        return Response(event_list, status=200)
    
    
class EventDetailStrategy(EventStrategy):
    """
    Strategy for retrieving details of a specific event.
    """
    def execute(self, event_id: int) -> EventResponseSchema:
        """
        Retrieve detailed information for a specific event, including engagement data.

        Args:
            event_id (int): The ID of the event.

        Returns:
            EventResponseSchema: The event details along with engagement data, user-specific engagement status,
            and updated event status.
        """
        self.autheticate_user()
        logger.info("Fetching details for event ID: %d by user %s.", event_id, self.request.user.username)
        event = get_object_or_404(Event, id=event_id)
        engagement_data = EventResponseSchema.resolve_engagement(event)
        user_engaged = EventResponseSchema.resolve_user_engagement(event, self.user)
        EventResponseSchema.set_status_event(event)

        event_data = EventResponseSchema.from_orm(event)
        event_data.engagement = engagement_data
        event_data.user_engaged = user_engaged
        return event_data
    
    
class EventEditStrategy(EventStrategy):
    """
    Strategy for editing an event.    
    """
    def execute(self, event_id : int, data):
        """
        Edit an existing event if the user is the organizer.

        Args:
            event_id (int): The ID of the event to be edited.
            data: The updated event data.

        Returns:
            Response: The updated event details with status code 200 if successful.
            Response: Error message with status code 403 if the user is not allowed to edit the event,
                    404 if the event or organizer does not exist, or 400 for other errors.
        """
        try:
            event = Event.objects.get(id=event_id)
            organizer = Organizer.objects.get(user=self.user)
            if event.organizer != organizer:
                logger.warning(f"User {self.user.username} tried to edit an event they do not own.")
                return Response({'error': 'You are not allowed to edit this event.'}, status=403)
            
            update_fields = data.dict(exclude_unset = True)
            for field, value in update_fields.items():
                setattr(event, field, value)
            event.save()
            event_data = EventUpdateSchema.from_orm(event)
            logger.info(f"Organizer {organizer.organizer_name} edited their event {event_id}.")
            return Response(event_data, status=200)
        except Event.DoesNotExist:
            logger.error(f"Event with ID {event_id} does not exist.")
            return Response({'error': 'Event not found'}, status=404)
        except Organizer.DoesNotExist:
            logger.error(f"User {self.user.username} is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=404)
        except Exception as e:
            logger.error(f"Error while editing event {event_id}: {str(e)}")
            return Response({'error': str(e)}, status=400)
        
        
class EventUploadImageStrategy(EventStrategy):
    """Strategy for uploading an image for an event."""
    def replace_old_image(self, old_filename):
        """
        Delete an existing image from S3.

        Args:
            old_filename (str): The key of the image file to be deleted in the S3 bucket.

        Returns:
            None

        Logs:
            Logs information about the deletion process. Logs an error if deletion fails.
        """
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
            
    def validate_image(self,event, organizer, file):
        """
        Validate an image before uploading it to S3.

        Args:
            event (Event): The event to which the image is to be uploaded.
            organizer (Organizer): The organizer uploading the image.
            file (UploadedFile): The image file to be uploaded.

        Raises:
            ValidationError: If the image is not of the correct type or is too large.
        """

        if event.organizer != organizer:
            raise ValidationError('You are not allowed to upload an image for this event.')
            
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise ValidationError('Invalid file type. Only JPEG and PNG are allowed.')
        
        if file.size > MAX_FILE_SIZE:
            raise ValidationError(f'File size exceeds the limit of {MAX_FILE_SIZE / (1024 * 1024)} MB.')
            

    
    def execute(self, event_id: int, file: UploadedFile) -> Response:
        """
        Upload an image for a specific event.

        Args:
            event_id (int): The ID of the event to upload an image for.
            file (UploadedFile): The image file to be uploaded.

        Returns:
            FileUploadResponseSchema: Details of the uploaded image, including URL, or an error response.
        """
        try:
            event = get_object_or_404(Event, id=event_id)
            organizer = Organizer.objects.get(user=self.user)

            try:
                self.validate_image(event, organizer, file)
            except ValidationError as validation_error:
                return Response({'error': str(validation_error.messages[0])}, status=400)

            if event.event_image:
                old_filename = event.event_image.url
                self.replace_old_image(old_filename)

            filename = f'event_images/{uuid.uuid4()}{os.path.splitext(file.name)[1]}'
            logger.info("Starting upload for file: %s", filename)

            try:
                self.upload_s3(file, filename)
                file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{filename}"
                logger.info("Successfully uploaded file to S3: %s", file_url)

                event.event_image = filename
                event.save()

                return Response(FileUploadResponseSchema(
                    file_url=file_url,
                    message="Upload successful",
                    file_name=os.path.basename(filename),
                    uploaded_at=timezone.now()
                ), status=200)

            except ClientError as client_error:
                logger.error("S3 upload error: %s", str(client_error))
                return Response({'error': f"S3 upload failed: {str(client_error)}"}, status=400)

        except Organizer.DoesNotExist:
            return Response({'error': 'User is not an organizer'}, status=404)
        except Exception as generic_error:
            return Response({'error': f"Upload failed: {str(generic_error)}"}, status=400)
        
        
        
    
class EventEngagement:
    """Base class for event engagement strategies."""
    def __init__(self, request, event_id):
        self.user = request.user
        self.event = get_object_or_404(Event, id=event_id)
        
    @staticmethod
    def get_engagement_strategy(strategy_name,request, event_id):
        """
        Retrieve the event engagement strategy based on the provided strategy name.

        Args:
            strategy_name (str): The name of the strategy to retrieve.
            request (HttpRequest): The HTTP request object containing user details.
            event_id (int): The ID of the event to be retrieved.

        Returns:
            An instance of the strategy corresponding to the given name,
            or None if the name is not recognized.
        """
        strategies = {
            'event_comment': EventCommentStrategy(request,event_id),
            'event_attendee': EventAllAttendee(request,event_id),
            'event_ticket' : EventAllTicket(request, event_id)
        }
        return strategies.get(strategy_name)
        
    
    @abstractmethod    
    def execute(self,event_id):
        """
        Execute the event engagement strategy based on the given event ID.

        Args:
            event_id (int): The ID of the event to be retrieved.

        Returns:
            The result of executing the strategy, which varies depending on the
            specific strategy being executed.

        Raises:
            400: If the request is invalid due to missing or invalid data.
            404: If the event does not exist.
            500: If an error occurs during the execution of the strategy.
        """
        pass
    


class EventCommentStrategy(EventEngagement):
    """Strategy to retrieve comments for an event."""
    def execute(self):
        """
        Execute the strategy to retrieve top-level comments for the event.

        Returns:
            Response: A response containing a list of serialized top-level comments
            for the event, including related user, replies, and reactions.
            The comments are ordered by creation date in descending order.
        """
        comments = Comment.objects.filter(event=self.event, parent=None).select_related('user').prefetch_related('replies', 'reactions').order_by('-created_at')
        response_data = [CommentResponseSchema.from_orm(comment) for comment in comments]
        logger.info(f"Retrieved {len(comments)} comments for event {self.event.id}.")
        return Response(response_data, status=200)
    
    
class EventAllAttendee(EventEngagement):
    """Strategy to retrieve all attendees for an event."""
    def execute(self):
        """
        Execute the strategy to retrieve all attendees for the event.

        Returns:
            Response: A response containing a list of serialized attendees for the event,
                ordered by username in ascending order. If the user is not an organizer of the event,
                a 403 error is raised with an appropriate error message.
        """
        try:
            organizer = Organizer.objects.get(user=self.user)
            if self.event.organizer != organizer:
                logger.warning(f"User {self.user.username} tried to access attendee list but is not an organizer.")
                return Response({'error': 'You are not allowed to access this event.'}, status=403)
            tickets = Ticket.objects.filter(event=self.event).order_by('attendee__username')
            response_data = [UserResponseSchema.from_orm(ticket.attendee) for ticket in tickets]
            logger.info(f"Retrieved attendee list for event {self.event.id}.")
            return Response(response_data, status=200)
        except Organizer.DoesNotExist:
            logger.error(f"User {self.user.username} tried to access attendee list but is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=403)
        
        
class EventAllTicket(EventEngagement):
    """Strategy to retrieve all tickets for an event."""
    def execute(self):
        """
        Execute the strategy to retrieve all tickets for the event.

        Returns:
            Response: A response containing a list of serialized tickets for the event, ordered by ticket ID.
        """
        tickets = Ticket.objects.filter(event=self.event).order_by('id')
        response_data = [TicketResponseSchema(
                            **ticket.get_ticket_details()
                        )
                        for ticket in tickets]
        logger.info(f"Retrieved ticket list for event {self.event.id}.")
        return Response(response_data, status=200)
        
        

        
    
    
        
        
    

