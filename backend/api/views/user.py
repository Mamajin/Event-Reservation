from .schemas import UserSchema, LoginResponseSchema, UserResponseSchema, LoginSchema, ErrorResponseSchema, FileUploadResponseSchema, AuthResponseSchema, GoogleAuthSchema
from .modules import *



router = Router()


class UserAPI:
            
    @router.post('/register', response={201: UserSchema, 400: ErrorResponseSchema})
    def create_user(request, form: UserSchema = Form(...)):
        if form.password != form.password2:
            return Response({"error": "Passwords do not match"}, status=400)
        if AttendeeUser.objects.filter(username = form.username).exists():
            return Response({"error": "Username already taken"}, status=400)
        if AttendeeUser.objects.filter(email = form.email).exists():
            return Response({"error": "This email already taken"}, status=400)
        try:
            user = AttendeeUser(username = form.username, password =make_password(form.password), birth_date = form.birth_date, 
                                           phone_number = form.phone_number, email = form.email, first_name = form.first_name, last_name = form.last_name)
        except Exception as e:
            return Exception
        user.save()
        return Response(UserSchema.from_orm(user), status=201)
    
    
    @router.post('/auth/google', response =  AuthResponseSchema)
    def google_auth(request, data : GoogleAuthSchema):
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
        user = authenticate(request, username = form.username, password = form.password)
        
        if user is not None:
            login(request,user)
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

            # Conditional inclusion of image_url
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

        
    @router.get('/profile', response=UserResponseSchema, auth = JWTAuth())
    def view_profile(request):
        """
        Retrieve the profile details of the currently logged-in user, 
        including their role (Organizer or Attendee).

        Returns:
            The user's profile information including username, tokens, 
            and role (Organizer or Attendee).
        """
        user = request.user

        profile_user = get_object_or_404(AttendeeUser, username = user.username)
        profile_dict = UserResponseSchema.from_orm(profile_user).dict()
        
        profile_data = UserResponseSchema(**profile_dict)

        return profile_data
    
    @router.put('/edit-profile/{user_id}/', response=UserResponseSchema, auth=  JWTAuth())
    def edit_profile(request, user_id : int, new_data : UserResponseSchema):
        AttendeeUser.objects.filter(id = user_id).update(**new_data.dict())
        user = AttendeeUser.objects.get(id = user_id)
        user_data = UserResponseSchema.from_orm(user).dict()
        return user_data
    
    @router.delete('delete/{user_id}/', auth=  JWTAuth())
    def delete_profile(request, user_id : int):
        user = request.user
        if AttendeeUser.objects.filter(id = user_id).exists():
            user = AttendeeUser.objects.get(id = user_id)
            user.delete()
            if Organizer.objects.filter(user = user).exists():
                organizer=  Organizer.objects.get(user = user)
                organizer.delete()
        return Response({'sucess': 'Your account has been deleted'})
    
    @router.post('/{user_id}/upload/profile-picture/', response={200: FileUploadResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())
    def upload_profile_picture(request: HttpRequest, user_id: int, profile_picture: UploadedFile = File(...)):
        """
        Upload an profile picture for a user by user I.
        """
        try:
            user = request.user
            
            if profile_picture.content_type not in ALLOWED_IMAGE_TYPES:
                return Response({'error': 'Invalid file type. Only JPEG and PNG are allowed.'}, status=400)
            
            if profile_picture.size > MAX_FILE_SIZE:
                return Response({'error': f'File size exceeds the limit of {MAX_FILE_SIZE / (1024 * 1024)} MB.'}, status=400)
            
            # Check if there's an existing image
            if user.profile_picture:
                old_filename = user.profile_picture.url
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
