from abc import ABC, abstractmethod
from api.views.modules import *
from api.views.schemas.event_schema import *
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
            return Response({'error': f"S3 upload failed"}, status=400)
        event.save()
        return EventResponseSchema.from_orm(event)
    
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
        
    

