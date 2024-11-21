from abc import ABC, abstractmethod
from api.views.modules import *
from api.views.schemas.user_schema import *
from api.views.schemas.other_schema import FileUploadResponseSchema


class UserStrategy(ABC):
    """
    Abstract base class for user-related strategies.
    """
    @staticmethod
    def get_strategy(strategy_name):
        """
        Retrieve the user-related strategy based on the provided strategy name.

        Args:
            strategy_name (str): The name of the strategy to retrieve.

        Returns:
            An instance of the strategy corresponding to the given strategy name,
            or None if the strategy name is not recognized.
        """
        strategies = {
            'user_register': UserRegisterStrategy(),
            'user_logout': UserlogoutStrategy(),
            'user_login': UserloginStrategy(),
            'user_google_login': UserGoogleAuthStrategy(),
            'user_view_profile': UserViewProfile(),
            'user_edit_profile': UserEditProfile(),
            'user_delete_account': UserDeleteAccount(),
            'user_upload_picture': UserUploadProfilePicture(),
            'user_verify_email' : UserVerifyEmail(),
            'user_resend_verification': UserResendVeification(),
        }
        return strategies.get(strategy_name)
    
    @abstractmethod
    def execute(self, *arg, **kwargs):
        """
        Executes the strategy based on the given arguments.

        Args:
            *arg: A variable length argument list.
            **kwargs: A dictionary of keyword arguments.

        Raises:
            NotImplementedError: If the execute method is not implemented in the
                derived class.
        """
        pass
    
    
class UserRegisterStrategy(UserStrategy):
    """ 
    Strategy for user registration. 
    """
    def validate_input_information(self, form):
        """
        Validates the input information from the registration form.

        Args:
            form: The user registration form containing input fields such as 
                username, password, email, and phone number.

        Raises:
            ValidationError: If the form is empty, passwords do not match, 
                            username or email is already taken, 
                            or required fields such as username, email, 
                            and phone number are missing or invalid.
        """
        if form is None:
            raise ValidationError('Form data is empty')

        if form.password != form.password2:
            raise ValidationError("Passwords do not match")

        if not form.username:
            raise ValidationError('Username is empty')

        if AttendeeUser.objects.filter(username=form.username).exists():
            raise ValidationError("Username already taken")

        if not form.email:
            raise ValidationError('Email is empty')

        if AttendeeUser.objects.filter(email = form.email).exists():
            raise ValidationError("This email already taken")

        if not form.phone_number:
            raise ValidationError('Phone number is empty')

        if len(form.phone_number) != 10:
            raise ValidationError('Phone number must be 10 digits long')

        if not form.phone_number.isdigit():
            raise ValidationError('Phone number must be digit')
    
    
    
    def execute(self, form):
        """
        Execute the user registration strategy. This method validates the form data, 
        creates a new user with the provided information, and sends an email to the user
        to verify their account.

        Args:
            form: The user registration form containing input fields such as 
                username, password, email, and phone number.

        Returns:
            A Response object containing the newly created user object if the operation
            is successful, or a Response object with a 400 error code containing an
            error message if the operation fails.
        """
        try: 
            self.validate_input_information(form)
        except ValidationError as e:
            return Response({'error': e.messages[0]}, status=400)
        
        user = AttendeeUser(
            username=form.username,
            password=make_password(form.password),
            birth_date=form.birth_date,
            phone_number=form.phone_number,
            email=form.email,
            first_name=form.first_name,
            last_name=form.last_name
        )
        user.save()
        user.send_verification_email()
        return Response(UserSchema.from_orm(user), status=201)
    
    
class UserlogoutStrategy(UserStrategy):
    """
    Strategy for user logout.
    """
    def execute(self, request):
        """
        Execute the user logout strategy. This method logs out the current user
        and returns a success message.

        Args:
            request: The HTTP request object containing user session information.

        Returns:
            Response: A response object with a success message and a 200 status code 
            indicating the user has been logged out successfully.
        """
        logout(request)
        return Response({"message": "Logged out successfully"}, status=200)
        

class UserloginStrategy(UserStrategy):
    """
    Strategy for user login.
    """
    def execute(self, request, form):
        """
        Authenticate and log in a user, returning access and refresh tokens along with user details.

        Args:
            request: The HTTP request object containing user credentials.
            form: A form object containing login details (username and password).

        Returns:
            Response: A response object containing tokens, user details, and a success message 
                    if authentication is successful, or an error message if authentication fails.
        """
        user = authenticate(request, username=form.username, password=form.password)
        if user is not None:
            login(request, user)
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            response_data = {
                "success": True,
                "message": "Login successful",
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
                "username": user.username,
                "id": user.id,
                "status": user.status,
            }

            if user.status == 'Organizer':
                try:
                    organizer = Organizer.objects.get(user=user)
                    response_data["image_url"] = organizer.logo.url if organizer.logo else None
                except Organizer.DoesNotExist:
                    response_data["image_url"] = None
            else:
                response_data["image_url"] = user.profile_picture.url if user.profile_picture else None

            return Response(response_data, status=200)
        else:
            return Response(
                {"error": "Invalid username or password"},
                status=400
            )
            
            
class UserGoogleAuthStrategy(UserStrategy):
    """
    Strategy for authenticating a user via Google OAuth2.
    """
    def execute(self, request ,data):
        """
        Authenticate a user via Google OAuth2 and retrieve access and refresh tokens.

        Args:
            request: The request object.
            data (GoogleAuthSchema): Google authentication token data.

        Returns:
            Response: A response containing user details and tokens on successful authentication.
        """
        idinfo = id_token.verify_oauth2_token(
            data.token, 
            requests.Request(),
            settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            clock_skew_in_seconds=10
            )
            
        email = idinfo.get('email')
        first_name  = idinfo.get('given_name')
        last_name = idinfo.get('family_name')
        picture = idinfo.get('picture')

        
        if AttendeeUser.objects.filter(email = email).exists():
            # User exists; optionally update user details from Google info
            user=  AttendeeUser.objects.get(email = email)
            first_name = user.first_name
            last_name = user.last_name
            email = user.email
        else:
            # Create a new user if one does not exist
            user = AttendeeUser.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                username=email.split('@')[0],  # Optionally use email prefix as username
                password=make_password(get_random_string(8)),  # Generate a random password
            )

        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        login(request,user)
        return Response(
            {   'id': user.id,
                'status': user.status,
                'refresh_token': str(refresh_token),
                'access_token': str(access_token),
                'first_name': str(first_name),
                'last_name': str(last_name),
                'picture': str(picture),
                'email' : str(email)
                }
        )
        
class UserViewProfile(UserStrategy):
    """
    Strategy for retrieving a user's profile information.
    """
    def execute(self, request):
        """
        Retrieve the profile information of the currently logged-in user.

        Args:
            request (HttpRequest): The request object.

        Returns:
            UserResponseSchema: The profile details of the user.
        """
        
        user = request.user
        profile_user = get_object_or_404(AttendeeUser, username=user.username)
        profile_dict = UserResponseSchema.from_orm(profile_user).dict()
        profile_data = UserResponseSchema(**profile_dict)
        return profile_data
            

class UserEditProfile(UserStrategy):
    """
    Strategy for updating a user's profile information.
    """
    def execute(self, user_id, new_data):
        """
        Update the profile information of a user by user ID.

        Args:
            user_id (int): The ID of the user to be updated.
            new_data (UserupdateSchema): New profile data for the user.

        Returns:
            UserupdateSchema: Updated user profile details.
        """
        user = get_object_or_404(AttendeeUser, id=user_id)
        update_fields = new_data.dict(exclude={'profile_picture'}, exclude_unset = True)
        for field, value in update_fields.items():
            setattr(user, field, value)
        user.save()
        user.refresh_from_db()
        return UserupdateSchema.from_orm(user)

class UserDeleteAccount(UserStrategy):
    """
    Strategy for deleting a user account.
    """
    def execute(self, request):
        """
        Delete a user account by user ID.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: A response containing a success message upon successful deletion.
        """

        user = request.user
        get_user = AttendeeUser.objects.get(id = user.id)

        get_user.delete()
            
        return Response({'success': 'Your account has been deleted'})
    
class UserUploadProfilePicture(UserStrategy):
    """
    Strategy for uploading a user's profile picture.
    """
    @staticmethod
    def upload_file_to_s3(user,filename, profile_picture):
        """
        Upload a file to S3 directly using boto3.

        Args:
            user (AttendeeUser): The user who is uploading the file.
            filename (str): The filename to use when uploading the file.
            profile_picture (UploadedFile): The file to be uploaded.

        Returns:
            Response: A response containing the uploaded file's details upon successful upload.
        """
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
                    profile_picture.file,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    filename,
                    ExtraArgs={
                        'ContentType': profile_picture.content_type,
                    }
                )

                file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{filename}"
                logger.info(f"Successfully uploaded file to S3: {file_url}")
                
                user.profile_picture = filename
                user.save()
            
                return Response(FileUploadResponseSchema(
                    file_url=file_url,
                    message="Upload successful",
                    file_name=os.path.basename(filename),
                    uploaded_at=timezone.now()
                ), status=200)
            
        except ClientError as e:
            logger.error(f"S3 upload error: {str(e)}")
            return Response({'error': f"S3 upload failed: {str(e)}"}, status=400)
            
    
    def execute(self, request, profile_picture):
        """
        Handles the upload of a user's profile picture to S3.

        Args:
            request (HttpRequest): The HTTP request containing the user and file information.
        profile_picture (UploadedFile): The profile picture file to be uploaded.

        Returns:
            Response: A response indicating success with file details or an error message if the upload fails.
        """
        try:
            user = request.user
            
            if profile_picture.content_type not in ALLOWED_IMAGE_TYPES:
                return Response({'error': 'Invalid file type. Only JPEG and PNG are allowed.'}, status=400)
            
            if profile_picture.size > MAX_FILE_SIZE:
                return Response({'error': f'File size exceeds the limit of {MAX_FILE_SIZE / (1024 * 1024)} MB.'}, status=400)

            filename = f'picture_profiles/{uuid.uuid4()}{os.path.splitext(profile_picture.name)[1]}'
            logger.info(f"Starting upload for file: {filename}")
            upload_file = self.upload_file_to_s3(user, filename, profile_picture)
            return upload_file

        except Exception as e:
            return Response({'error': f"Upload failed: {str(e)}"}, status=400)
        
    
class UserVerifyEmail(UserStrategy):
    """
    Strategy for verifying a user's email address.
    """
    def execute(self,user_id,token):
        """
        Verify a user's email address using a verification token.

        Args:
            user_id (str): The ID of the user to verify.
            token (str): The verification token sent to the user's email address.

        Returns:
            Response: A response indicating success if the token is valid and not expired, or an error message if the token is invalid or expired.
        """

        try:
            uid = force_str(urlsafe_base64_decode(user_id))
            user = AttendeeUser.objects.get(pk=uid)
            
            # Check if token is valid and user is not yet verified
            if default_token_generator.check_token(user, token) and not user.is_email_verified:
                user.is_email_verified = True
                user.is_active = True
                user.save()
                
                return Response({
                    "message": "Email verified successfully",
                    "verified": True
                }, status=200)
            else:
                return Response({
                    "error": "Invalid or expired token"
                }, status=400)
        except (TypeError, ValueError, OverflowError, AttendeeUser.DoesNotExist):
            return Response({
                "error": "Invalid verification token"
            }, status=400)
            
class UserResendVeification(UserStrategy):
    """
    Strategy for resending a verification email to a user.
    """
    def execute(self, email):
        """
        Resend a verification email to a user with the given email address.

        Args:
            email (str): The email address of the user to resend the verification email to.

        Returns:
            Response: A response indicating success if the email is sent successfully, or an error message if the user is not found or already verified.
        """
        try:
            user = AttendeeUser.objects.get(email=email, is_email_verified=False)
            user.send_verification_email()
            
            return Response({
                "message": "Verification email sent successfully",
                "verified": user.is_email_verified
            }, status=200)
        except AttendeeUser.DoesNotExist:
            return Response({
                "error": "User not found or already verified"
            }, status=400)

