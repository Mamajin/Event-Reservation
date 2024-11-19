from abc import ABC, abstractmethod
from api.views.modules import *
from api.views.schemas import *
from injector import inject


class EventStrategy:
    

    def __init__(self, request: HttpRequest):
        self.user = request.user
        self.request = request

    

    @staticmethod
    def get_strategy(strategy_name, request):
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
        pass
    
    def upload_image(self,image,event):
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
    
    def add_event(self,event_list: list,events):
        for event in events:
                engagement = EventResponseSchema.resolve_engagement(event)
                user_engaged = EventResponseSchema.resolve_user_engagement(event, self.user)
                EventResponseSchema.set_status_event(event)
                event_data = EventResponseSchema.from_orm(event)
                event_data.engagement = engagement
                event_data.user_engaged = user_engaged
                event_list.append(event_data)
                
                
    def autheticate_user(self):
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
    
            
    def execute(self, data: EventInputSchema = Form(...), image : UploadedFile = File(None)):
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

        
    def execute(self):
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
    
    def execute(self):
        events = Event.objects.filter(event_create_date__lte=timezone.now()).order_by("-event_create_date")
        event_list = []
        self.autheticate_user()

        self.add_event(event_list,events)

        # Conditionally add user-specific engagement data

        logger.info("Retrieved all public events for the homepage.")
        return Response(event_list, status=200)
    
    
class EventDetailStrategy(EventStrategy):
    
    def execute(self,event_id):
        self.autheticate_user()
        logger.info(f"Fetching details for event ID: {event_id} by user {self.request.user.username}.")
        event = get_object_or_404(Event, id=event_id)
        engagement_data = EventResponseSchema.resolve_engagement(event)
        user_engaged = EventResponseSchema.resolve_user_engagement(event, self.user)
        EventResponseSchema.set_status_event(event)
        
        event_data = EventResponseSchema.from_orm(event)
        event_data.engagement = engagement_data
        event_data.user_engaged = user_engaged
        return event_data
    
    
class EventEditStrategy(EventStrategy):
    
    def execute(self, event_id : int, data):
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
    
    def replace_old_image(self, old_filename):
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
        if event.organizer != organizer:
            raise ValidationError('You are not allowed to upload an image for this event.')
            
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise ValidationError('Invalid file type. Only JPEG and PNG are allowed.')
        
        if file.size > MAX_FILE_SIZE:
            raise ValidationError(f'File size exceeds the limit of {MAX_FILE_SIZE / (1024 * 1024)} MB.')
            

    
    def execute(self, event_id, file):
        try:
            event = get_object_or_404(Event, id=event_id)

            organizer = Organizer.objects.get(user=self.user)
            try:
                self.validate_image(event, organizer, file)
            except ValidationError as e:
                return Response({'error': str(e.messages[0])}, status=400)
            
            # Check if there's an existing image
            if event.event_image:
                old_filename = event.event_image.url
                self.replace_old_image(old_filename)

            filename = f'event_images/{uuid.uuid4()}{os.path.splitext(file.name)[1]}'
            logger.info(f"Starting upload for file: {filename}")
            try:
                # Direct S3 upload using boto3
                self.upload_s3(file,filename)

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
        
        
        
    
class EventEngagement:

    def __init__(self, request, event_id):
        self.user = request.user
        self.event = get_object_or_404(Event, id=event_id)
        
    @staticmethod
    def get_engagement_strategy(strategy_name,request, event_id):
        strategies = {
            'event_engagement': EventGetEngagementStrategy(request,event_id),
            'event_user_engagement': EventUserEngagementStrategy(request,event_id),
            'event_comment': EventCommentStrategy(request,event_id),
            'event_attendee': EventAllAttendee(request,event_id),
            'event_ticket' : EventAllTicket(request, event_id)
        }
        return strategies.get(strategy_name)
        
    
    @abstractmethod    
    def execute(self,event_id):
        pass
    
class EventGetEngagementStrategy(EventEngagement):
    
    def execute(self):
        engagement_data = EventResponseSchema.resolve_engagement(self.event)
        return engagement_data  
    
    
class EventUserEngagementStrategy(EventEngagement):
    
    def execute(self):
        user_engaged = EventResponseSchema.resolve_user_engagement(self.event, self.user)
        return user_engaged      


class EventCommentStrategy(EventEngagement):
    
    def execute(self):
        comments = Comment.objects.filter(event=self.event, parent=None).select_related('user').prefetch_related('replies', 'reactions').order_by('-created_at')
        response_data = [CommentResponseSchema.from_orm(comment) for comment in comments]
        logger.info(f"Retrieved {len(comments)} comments for event {self.event.id}.")
        return Response(response_data, status=200)
    
    
class EventAllAttendee(EventEngagement):
    
    def execute(self):
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
    
    def execute(self):
        tickets = Ticket.objects.filter(event=self.event).order_by('id')
        response_data = [TicketResponseSchema(
                            **ticket.get_ticket_details()
                        )
                        for ticket in tickets]
        logger.info(f"Retrieved ticket list for event {self.event.id}.")
        return Response(response_data, status=200)
        
        

        
    
    
        
        
    

