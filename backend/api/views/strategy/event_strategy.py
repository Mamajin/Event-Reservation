from abc import ABC, abstractmethod
from api.views.modules import *
from api.views.schemas import *


class EventStrategy(ABC):
    
    @staticmethod
    def get_strategy(strategy_name):
        strategies = {
            'create_event': EventCreateStrategy(),
            # 'get_ticket_detail': TicketGetTicketDetail(),
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
    
    
class EventCreateStrategy(EventStrategy):
    
    def execute(self, request, data: EventInputSchema = Form(...), image : UploadedFile = File(None)):
        this_user = request.user
        try:
            organizer = Organizer.objects.get(user=this_user)
        except Organizer.DoesNotExist:
            raise HttpError(status_code=403, message="You are not an organizer.")
        
        # Create event
        event = Event(**data.dict(), organizer=organizer)
        if not event.is_valid_date():
            return Response({'error': 'Please enter valid date'}, status=400)
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
                return Response({'error': f"S3 upload failed"}, status=400)
        event.save()
        return EventResponseSchema.from_orm(event)
    

