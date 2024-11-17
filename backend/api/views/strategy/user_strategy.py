from abc import ABC, abstractmethod
from api.views.modules import *
from api.views.schemas import *


class UserStrategy(ABC):
    
    @staticmethod
    def get_strategy(strategy_name):
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
        pass
    
    
class UserRegisterStrategy(UserStrategy):
    
    def validate_input_information(self, form):
        """Validate conditions for event registration."""
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
    
    def execute(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=200)
        

class UserloginStrategy(UserStrategy):
    
    def execute(self, request, form):
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
    
    def execute(self, request ,data):
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
    
    def execute(self, request):
        user = request.user
        profile_user = get_object_or_404(AttendeeUser, username=user.username)
        profile_dict = UserResponseSchema.from_orm(profile_user).dict()
        profile_data = UserResponseSchema(**profile_dict)
        return profile_data
            

class UserEditProfile(UserStrategy):
    
    def execute(self, user_id, new_data):
        user = get_object_or_404(AttendeeUser, id=user_id)
        update_fields = new_data.dict(exclude={'profile_picture'}, exclude_unset = True)
        for field, value in update_fields.items():
            setattr(user, field, value)
        user.save()
        user.refresh_from_db()
        return UserupdateSchema.from_orm(user)

class UserDeleteAccount(UserStrategy):
    
    def execute(self, request):
        user = request.user
        get_user = AttendeeUser.objects.get(id = user.id)

        get_user.delete()
            
        return Response({'success': 'Your account has been deleted'})
    
class UserUploadProfilePicture(UserStrategy):
    
    def execute(self, request,profile_picture):
        try:
            user = request.user
            
            if profile_picture.content_type not in ALLOWED_IMAGE_TYPES:
                return Response({'error': 'Invalid file type. Only JPEG and PNG are allowed.'}, status=400)
            
            if profile_picture.size > MAX_FILE_SIZE:
                return Response({'error': f'File size exceeds the limit of {MAX_FILE_SIZE / (1024 * 1024)} MB.'}, status=400)

            filename = f'picture_profiles/{uuid.uuid4()}{os.path.splitext(profile_picture.name)[1]}'
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
            
        except Exception as e:
            return Response({'error': f"Upload failed: {str(e)}"}, status=400)
        
    
class UserVerifyEmail(UserStrategy):
    
    def execute(self,user_id,token):
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
    
    def execute(self, email):
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

