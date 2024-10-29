from .schemas import UserSchema, LoginResponseSchema, UserResponseSchema, LoginSchema, ErrorResponseSchema
from .modules import AttendeeUser, Form, make_password, authenticate, login, AccessToken, RefreshToken,Response, JWTAuth, Organizer, status,get_object_or_404, Router

router = Router()



class UserAPI:
            
    @router.post('/register', response={201: None, 400: ErrorResponseSchema})
    def create_user(request, form: UserSchema = Form(...)):
        if form.password != form.password2:
            return Response({"error": "Passwords do not match"}, status=400)
        if AttendeeUser.objects.filter(username = form.username).exists():
            return Response({"error": "Username already taken"}, status=400)
        user = AttendeeUser.objects.create(username = form.username, password =make_password(form.password), birth_date = form.birth_date, 
                                           phone_number = form.phone_number, email = form.email, first_name = form.first_name, last_name = form.last_name)
        return Response({"username": user.username}, status=201)
    
    @router.post('/login', response = LoginResponseSchema)
    def login(request, form: LoginSchema = Form(...)):
        user = authenticate(request, username = form.username, password = form.password)
        
        if Organizer.objects.filter(user = user).exists():
            status = "Organizer"
        else:
            status = "Attendee"
            
        if user is not None:
            login(request,user)
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "message": "Login successful",
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
                "username": user.username,
                "password": user.password,
                "id" : user.id,
                "status": status,
            })
        else:
            return Response(
            {"error": "Invalid username or password"},
            status= 400)

        
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
        
        profile_data = UserResponseSchema(
            id=profile_user.id,
            username=profile_user.username,
            first_name=profile_user.first_name,
            last_name=profile_user.last_name,
            birth_date=profile_user.birth_date,
            phone_number=profile_user.phone_number,
            email=profile_user.email,
            status=profile_user.status,
        )

        return profile_data
