from api.views.modules import *
from api.views.schemas.organizer_schema import *
from api.views.schemas.other_schema import FileUploadResponseSchema


logger = logging.getLogger(__name__)

class OrganizerStrategy(ABC):
    """
    Abstract base class for organizer operations.
    """
    
    @staticmethod
    def get_strategy(name):
        """
        Retrieve the organizer-related strategy based on the provided strategy name.

        Args:
            name (str): The name of the strategy to retrieve.

        Returns:
            An instance of the strategy corresponding to the given name,
            or None if the name is not recognized.
        """
        strategies = {
            'apply_organizer': ApplyOrganizerStrategy(),
            'delete_event': DeleteEventStrategy(),
            'view_organizer': ViewOrganizerStrategy(),
            'update_organizer': UpdateOrganizerStrategy(),
            'revoke_organizer': RevokeOrganizerStrategy(),
            'upload_logo': UploadLogoStrategy(),
        }
        return strategies.get(name)
    
    @abstractmethod
    def execute(self, request: HttpRequest):
        """
        Execute the organizer-related operation.

        Args:
            request (HttpRequest): The HTTP request object, containing user and request metadata.

        Raises:
            NotImplementedError: If the execute method is not implemented in the derived class.
        """
        pass

class ApplyOrganizerStrategy(OrganizerStrategy):
    """Apply to be an organizer"""
    
    def execute(self, request: HttpRequest, form: OrganizerSchema = Form(...)):
        """
        Apply to be an organizer

        Args:
            request (HttpRequest): The HTTP request object.
            form (OrganizerSchema): The organizer registration data.

        Returns:
            OrganizerResponseSchema: The created organizer object on successful registration.
        """
        
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
    
    def execute(self, request: HttpRequest, event_id: int):
        """
        Delete an event by the authenticated organizer.

        Args:
            request (HttpRequest): The HTTP request object containing user details.
            event_id (int): The ID of the event to be deleted.

        Returns:
            Response: A success message with status code 204 if the event is deleted.
            ErrorResponseSchema: Error message with status code 403 if the user is not an organizer,
            or 404 if the event does not exist or the user does not have permission to delete it.
        """
        logger.info(f"User {request.user.id} is attempting to delete an event.")
        try:
            organizer = Organizer.objects.get(user=request.user)
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
    
    def execute(self, request: HttpRequest, data: OrganizerUpdateSchema):
        """
        Update the profile information of the authenticated organizer.

        Args:
            request (HttpRequest): The HTTP request object containing user details.
            data (OrganizerUpdateSchema): The updated organizer data.

        Returns:
            Response: A success message with status code 200 if the organizer is updated.
            ErrorResponseSchema: Error message with status code 400 if the organizer name is already taken,
            or 404 if the organizer profile does not exist.
        """
        logger.info(f"User {request.user.id} is attempting to update their organizer profile.")
        try:
            organizer = get_object_or_404(Organizer, user=request.user)

            if data.organizer_name and Organizer.objects.filter(organizer_name=data.organizer_name).exclude(user=request.user).exists():
                logger.info(f"Organizer name '{data.organizer_name}' is already taken.")
                return Response({'error': 'Organizer name is already taken'}, status=400)
            
            update_fields = data.dict(exclude_unset=True)
            for field, value in update_fields.items():
                setattr(organizer, field, value)
            
            organizer.full_clean(exclude=['logo'])
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
    
    def execute(self, request: HttpRequest):
        """
        Revoke an organizer role.

        Args:
            request (HttpRequest): The HTTP request object containing user details.

        Returns:
            Response: A success message with status code 200 if the organizer role is revoked.
            ErrorResponseSchema: Error message with status code 404 if the user is not an organizer,
            or 400 if there is an error revoking the organizer role.
        """
        logger.info(f"User {request.user.id} is attempting to revoke their organizer role.")

        try:
            organizer = Organizer.objects.get(user=request.user)
            organizer.delete()
            logger.info(f"Organizer role revoked for user {request.user.id}.")
            return Response({'success': f'Organizer role revoked for user {request.user.id}.'}, status=200)
        
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} tried to revoke a non-existing organizer profile.")
            return Response({'error': 'User is not an organizer'}, status=404)
        except Exception as e:
            logger.error(f"Error revoking organizer role: {str(e)}")
            return Response({'error': str(e)}, status=400)


class ViewOrganizerStrategy(OrganizerStrategy):
    """View an organizer profile"""
    
    def execute(self, request: HttpRequest):
        """
        Retrieve the profile information of the authenticated organizer.

        Args:
            request (HttpRequest): The HTTP request object containing user details.

        Returns:
            Response: Organizer profile details if successful with status code 200.
            ErrorResponseSchema: Error message with status code 404 if the user is not an organizer,
            or 400 in case of other errors.
        """
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
    ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg']
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    def _delete_existing_logo(self, old_filename):
        """
        Delete an existing logo from S3.

        Args:
            old_filename (str): The name of the existing logo file to be deleted.

        Returns:
            None
        """
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
        """
        Upload a file to S3 directly using boto3.

        Args:
            file_obj (File): The file to be uploaded.
            filename (str): The filename to use when uploading the file.

        Returns:
            str: The URL of the uploaded file.
        """
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

    def execute(self, request: HttpRequest, organizer_id: int, logo: UploadedFile = File(...)):
        """
        Upload a logo for an organizer.

        Args:
            request (HttpRequest): The HTTP request object.
            organizer_id (int): The ID of the organizer to upload a logo for.
            logo (UploadedFile): The logo file to be uploaded.

        Returns:
            Response: A response indicating success with file details or an error response if the upload fails.
        """
        try:
            organizer = get_object_or_404(Organizer, id=organizer_id)

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
            ).dict(), status=200)

        except Exception as e:
            logger.error(f"Upload failed: {str(e)}")
            return Response({'error': f"Upload failed: {str(e)}"}, status=400)
