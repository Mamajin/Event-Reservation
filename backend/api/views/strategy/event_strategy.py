from abc import ABC, abstractmethod
from api.views.modules import *
from api.views.schemas import *
from injector import inject


class EventStrategy:
    

    def __init__(self, request: HttpRequest):
        self.user = request.user

    

    @staticmethod
    def get_strategy(strategy_name, request):
        strategies = {
            'create_event': EventCreateStrategy(request),
            'organizer_get_events': EventOrganizerStrategy(request),
            # 'register_ticket': TicketRegisterStrategy(),
            # 'cancel_ticket': TicketDeleteStrategy(),
            # 'sent_reminder': TicketSendReminderStrategy(),
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

    
    def add_event(self,event_list: list,events):
        for event in events:
                engagement = EventResponseSchema.resolve_engagement(event)
                user_engaged = EventResponseSchema.resolve_user_engagement(event, self.user)
                EventResponseSchema.set_status_event(event)
                event_data = EventResponseSchema.from_orm(event)
                event_data.engagement = engagement
                event_data.user_engaged = user_engaged
                event_list.append(event_data)
        
    
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
    

