from api.views.modules import *
from api.views.schemas import *


logger = logging.getLogger(__name__)

class OrganizerStrategy(ABC):
    """Abstract base class for organizer operations"""
    
    @abstractmethod
    def get_strategy(name):
        """Get the strategy based on the name"""
        pass
    
    @abstractmethod
    def execute(self, request: HttpRequest, **kwargs):
        """Execute the strategy"""
        pass

class ApplyOrganizerStrategy(OrganizerStrategy):
    """Apply to be an organizer"""
    
    @staticmethod
    def get_strategy(name):
        """Get the strategy based on the name"""
        if name != 'apply_organizer':
            return
        return ApplyOrganizerStrategy()
    
    def execute(self, request: HttpRequest, form: OrganizerSchema = Form(...), **kwargs):
        """Apply to be an organizer"""
        try:
            logger.info(f"User {request.user.id} is attempting to apply as an organizer.")
            
            if Organizer.objects.filter(user=request.user).exists():
                logger.info(f"User {request.user.id} already has an organizer profile.")
                return Response({"error": "User is already an organizer"}, status=400)

            organizer_name = form.organizer_name or ""
            
            if organizer_name and Organizer.objects.filter(organizer_name=organizer_name).exists():
                logger.info(f"Organizer name '{organizer_name}' is already taken.")
                return Response({"error": "Organizer name is already taken"}, status=400)

            organizer = Organizer(
                user=request.user,
                organizer_name=organizer_name,
                email=form.email or request.user.email,
                organization_type=form.organization_type,
            )
            
            organizer.full_clean()
            organizer.save()
            
            request.user.status = "Organizer"
            request.user.save()
            
            logger.info(f"User {request.user.id} successfully applied as organizer with ID {organizer.id}.")
            
            return Response(OrganizerResponseSchema.from_orm(organizer), status=201)
            
        except Exception as e:
            logger.error(f"Unexpected error while creating organizer for user {request.user.id}: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=400)

class DeleteEventStrategy(OrganizerStrategy):
    """Delete an event"""
    
    @staticmethod
    def get_strategy(name):
        """Get the strategy based on the name"""
        if name != 'delete_event':
            return
        return DeleteEventStrategy()
    
    def execute(self, request: HttpRequest, event_id: int, **kwargs):
        """Delete an event"""
        logger.info(f"User {request.user.id} is attempting to delete an event.")
        try:
            organizer = get_object_or_404(Organizer, user=request.user)
            event = get_object_or_404(Event, id=event_id, organizer=organizer)
            event.delete()
            logger.info(f"Organizer {organizer.organizer_name} deleted event {event_id}.")
            return Response({'success': f"Delete event ID {event_id} successfully"}, status=204)
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} attempted to delete event {event_id} but is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=403)
        except Event.DoesNotExist:
            logger.error(f"Organizer {organizer.organizer_name} attempted to delete non-existing event {event_id}.")
            return Response({'error': 'Event does not exist or you do not have permission to delete it'}, status=404)

class UpdateOrganizerStrategy(OrganizerStrategy):
    """Update an organizer profile"""
    
    @staticmethod
    def get_strategy(name):
        """Get the strategy based on the name"""
        if name != 'update_organizer':
            return
        return UpdateOrganizerStrategy()
    
    def execute(self, request: HttpRequest, data: OrganizerUpdateSchema, **kwargs):
        """Update the profile information of the authenticated organizer."""
        logger.info(f"User {request.user.id} is attempting to update their organizer profile.")
        try:
            organizer = get_object_or_404(Organizer, user=request.user)

            if data.organizer_name == organizer.organizer_name and Organizer.objects.filter(organizer_name=data.organizer_name).exists():
                logger.info(f"Organizer name '{data.organizer_name}' is already taken.")
                return Response({'error': 'Organizer name is already taken'}, status=400)
            
            update_fields = data.dict(exclude_unset=True)
            for field, value in update_fields.items():
                setattr(organizer, field, value)
            
            organizer.save()
            
            logger.info(f"User {request.user.id} updated their organizer profile.")
            return Response(OrganizerUpdateSchema.from_orm(organizer).dict(), status=200)
            
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.id} attempted to update non-existing organizer profile.")
            return Response({'error': 'Organizer profile does not exist'}, status=404)
        except Exception as e:
            logger.error(f"Error updating organizer profile: {str(e)}")
            return Response({'error': str(e)}, status=400)

class RevokeOrganizerStrategy(OrganizerStrategy):
    """Revoke an organizer role"""
    @staticmethod
    def get_strategy(name):
        """Get the strategy based on the name"""
        if name != 'revoke_organizer':
            return
        return RevokeOrganizerStrategy()
    
    def execute(self, request: HttpRequest, **kwargs):
        """Revoke the organizer role of the authenticated user."""
        logger.info(f"User {request.user.id} is attempting to revoke their organizer role.")
        try:
            organizer = get_object_or_404(Organizer, user=request.user)
            organizer.delete()
            logger.info(f"Organizer role revoked for user {request.user.id}.")
            return Response({'success': f'Organizer role revoked for user {request.user.id}.'}, status=204)
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} tried to revoke a non-existing organizer profile.")
            return Response({'error': 'User is not an organizer'}, status=404)

class ViewOrganizerStrategy(OrganizerStrategy):
    """View an organizer profile"""
    
    @staticmethod
    def get_strategy(name):
        """Get the strategy based on the name"""
        if name != 'view_organizer':
            return
        return ViewOrganizerStrategy()
    
    def execute(self, request: HttpRequest, **kwargs):
        """View the organizer profile."""
        logger.info(f"User {request.user.id} is attempting to view their organizer profile.")
        try:
            organizer = get_object_or_404(Organizer, user=request.user)
            logger.info(f"User {request.user.id} viewed their organizer profile.")
            return Response(OrganizerResponseSchema.from_orm(organizer), status=200)
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} tried to view a non-existing organizer profile.")
            return Response({'error': 'User is not an organizer'}, status=404)
        except Exception as e:
            logger.error(f"Error viewing organizer profile: {str(e)}")
            return Response({'error': str(e)}, status=400)

class UploadLogoStrategy(OrganizerStrategy):
    """Upload a logo for an organizer"""
    ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png']
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    @staticmethod
    def get_strategy(name):
        """Get the strategy based on the name"""
        if name != 'upload_logo':
            return
        return UploadLogoStrategy()
    
    def _delete_existing_logo(self, old_filename):
        """Delete the old logo from S3"""
        logger.info(f"Deleting old image from S3: {old_filename}")
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=old_filename)
            logger.info(f"Deleted old image from S3: {old_filename}")
        except ClientError as e:
            logger.error(f"Failed to delete old image from S3: {str(e)}")

    def _upload_to_s3(self, file_obj, filename):
        """Upload a file to S3"""
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )

            s3_client.upload_fileobj(
                file_obj,
                settings.AWS_STORAGE_BUCKET_NAME,
                filename,
                ExtraArgs={'ContentType': file_obj.content_type}
            )

            file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{filename}"
            logger.info(f"Successfully uploaded file to S3: {file_url}")
            return file_url

        except ClientError as e:
            logger.error(f"S3 upload error: {str(e)}")
            raise

    def execute(self, request: HttpRequest, **kwargs):
        """Upload a logo for an organizer"""    
        try:
            organizer_id = kwargs.get('organizer_id')
            organizer = get_object_or_404(Organizer, id=organizer_id)
            logo = request.FILES.get('logo')

            if not logo:
                return Response({'error': 'No file provided'}, status=400)

            if logo.content_type not in self.ALLOWED_IMAGE_TYPES:
                return Response({'error': 'Invalid file type. Only JPEG and PNG are allowed.'}, status=400)

            if logo.size > self.MAX_FILE_SIZE:
                return Response(
                    {'error': f'File size exceeds the limit of {self.MAX_FILE_SIZE / (1024 * 1024)} MB.'}, 
                    status=400
                )

            if organizer.logo:
                self._delete_existing_logo(organizer.logo.url)

            filename = f'logos/{uuid.uuid4()}{os.path.splitext(logo.name)[1]}'
            file_url = self._upload_to_s3(logo, filename)

            organizer.logo = filename
            organizer.save()

            return Response(FileUploadResponseSchema(
                file_url=file_url,
                message="Upload successful",
                file_name=os.path.basename(filename),
                uploaded_at=timezone.now()
            ), status=200)

        except Exception as e:
            logger.error(f"Upload failed: {str(e)}")
            return Response({'error': f"Upload failed: {str(e)}"}, status=400)
