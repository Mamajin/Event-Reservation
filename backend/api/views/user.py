from .schemas import UserSchema, LoginResponseSchema, UserResponseSchema, LoginSchema, ErrorResponseSchema, FileUploadResponseSchema, AuthResponseSchema, GoogleAuthSchema, EmailVerification, EmailVerificationResponseSchema
from .modules import *

router = Router()

class UserAPI:
    
    @router.post('/register', response={201: UserSchema, 400: ErrorResponseSchema})
    def create_user(request, form: UserSchema = Form(...)):
        """
        Register a new user with the provided details.

        Args:
            request: The request object.
            form (UserSchema): The schema containing user registration details.

        Returns:
            Response: Success response with user data on successful registration, or
                      an error message if registration fails.
        """
        if form.password != form.password2:
            return Response({"error": "Passwords do not match"}, status=400)
        if AttendeeUser.objects.filter(username=form.username).exists():
            return Response({"error": "Username already taken"}, status=400)
        if AttendeeUser.objects.filter(email = form.email).exists():
            return Response({"error": "This email already taken"}, status=400)
        try:
            user = AttendeeUser(
                username=form.username,
                password=make_password(form.password),
                birth_date=form.birth_date,
                phone_number=form.phone_number,
                email=form.email,
                first_name=form.first_name,
                last_name=form.last_name,
                is_active=False
            )
            user.save()
            user.send_verification_email()
            return Response({
                **UserSchema.from_orm(user).dict(),
                "message": "Registration successful. Please check your email to verify your account."
            }, status=201)
        except IntegrityError:
            return Response({"error": "A user with this email or username already exists."}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        # return Response(UserSchema.from_orm(user), status=201)

    @router.post('/auth/google', response=AuthResponseSchema)
    def google_auth(request, data: GoogleAuthSchema):
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
            {'status': user.status,
                'refresh_token': str(refresh_token),
                'access_token': str(access_token),
                'first_name': str(first_name),
                'last_name': str(last_name),
                'picture': str(picture),
                'email' : str(email)
                }
        )
                    
    
    @router.post('/login', response = LoginResponseSchema)
    def login(request, form: LoginSchema = Form(...)):
        """
        Log in a user with username and password, returning access and refresh tokens.

        Args:
            request: The request object.
            form (LoginSchema): The login details (username and password).

        Returns:
            Response: A response containing tokens and user details upon successful login.
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

    @router.get('/profile', response=UserResponseSchema, auth=JWTAuth())
    def view_profile(request):
        """
        Retrieve the profile of the currently logged-in user.

        Returns:
            UserResponseSchema: The profile details of the user.
        """
        user = request.user
        profile_user = get_object_or_404(AttendeeUser, username=user.username)
        profile_dict = UserResponseSchema.from_orm(profile_user).dict()
        profile_data = UserResponseSchema(**profile_dict)
        return profile_data

    @router.put('/edit-profile/{user_id}/', response=UserResponseSchema, auth=JWTAuth())
    def edit_profile(request, user_id: int, new_data: UserResponseSchema):
        """
        Update the profile information of a user by user ID.

        Args:
            request: The request object.
            user_id (int): The ID of the user to be updated.
            new_data (UserResponseSchema): New profile data for the user.

        Returns:
            UserResponseSchema: Updated user profile details.
        """
        user = get_object_or_404(AttendeeUser, id=user_id)
        update_fields = new_data.dict(exclude={'profile_picture'})
        for field, value in update_fields.items():
            setattr(user, field, value)
        user.save()
        user.refresh_from_db()
        return UserResponseSchema.from_orm(user)

    @router.delete('delete/{user_id}/', auth=JWTAuth())
    def delete_profile(request, user_id: int):
        """
        Delete a user profile by user ID.

        Args:
            request: The request object.
            user_id (int): The ID of the user to delete.

        Returns:
            Response: Success message upon successful deletion.
        """
        user = request.user
        if AttendeeUser.objects.filter(id=user_id).exists():
            user = AttendeeUser.objects.get(id=user_id)
            user.delete()
            if Organizer.objects.filter(user=user).exists():
                organizer = Organizer.objects.get(user=user)
                organizer.delete()
        return Response({'success': 'Your account has been deleted'})

    @router.post('/{user_id}/upload/profile-picture/', response={200: FileUploadResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())
    def upload_profile_picture(request: HttpRequest, user_id: int, profile_picture: UploadedFile = File(...)):
        """
        Upload a profile picture for the specified user.

        Args:
            request (HttpRequest): The request object containing the file.
            user_id (int): The ID of the user for whom the profile picture is uploaded.
            profile_picture (UploadedFile): The uploaded profile picture file.

        Returns:
            Response: URL and details of the uploaded profile picture.
        """
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
        
    @router.get('/verify-email/{user_id}/{token}', response={200: EmailVerificationResponseSchema, 400: ErrorResponseSchema})
    def verify_email(request, user_id: str, token: str):
        """Verify user's email address with the secure token."""
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


    @router.post('/resend-verification', response={200: EmailVerificationResponseSchema, 400: ErrorResponseSchema})
    def resend_verification(request, email: str):
        """Resend verification email if user is not verified."""
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
            
    @router.post("/send-email")
    def send_email(request):
        subject = "Test Email"
        message = "This is a test email sent from Django Ninja."
        html_message = f"""
        <html>
            <body>
                <p>Hi,</p>
                <p>Thank you for registering! Please click the link below to verify your email address:</p>
                <a href="">Verify Email</a>
                <p>If you didn’t sign up, please ignore this email.</p>
            </body>
        </html>
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['ganzch04@gmail.com']  # Replace with actual recipient

        # Attempt to send the email
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return {"status": "Email sent successfully"}
        except Exception as e:
            return {"status": "Email failed to send", "error": str(e)}
