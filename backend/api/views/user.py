from .schemas import UserSchema, LoginResponseSchema, UserResponseSchema, LoginSchema
from .modules import AttendeeUser, Form, make_password, authenticate, login, AccessToken, RefreshToken,Response, JWTAuth, Organizer, status,get_object_or_404, Router

router = Router()



class UserAPI:
    

            
    @router.post('/register')
    def create_user(request, form: UserSchema = Form(...)):
        if form.password != form.password2:
            return {"error": "Passwords do not match"}
        if AttendeeUser.objects.filter(username = form.username).exists():
            return {"error": "Username already taken"}
        user = AttendeeUser.objects.create(username = form.username, password =make_password(form.password), birth_date = form.birth_date, 
                                           phone_number = form.phone_number, email = form.email, first_name = form.first_name, last_name = form.last_name)
        return {"username":user.username}
    
    
    
    @router.post('/login', response = LoginResponseSchema)
    def login(request, form: LoginSchema = Form(...)):
        user = authenticate(request, username = form.username, password = form.password)
            
        if user is not None:
            login(request,user)
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            return {
                "success": True,
                "message": "Login successful",
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
                "username": user.username,
                "password": user.password,
                "id" : user.id
            }
        else:
            return Response(
            {"success": False, "message": "Invalid username or password"},
            status=status.HTTP_403_FORBIDDEN
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
        if not user.is_authenticated:
            return Response(
                {"error": "User is not authenticated"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if Organizer.objects.filter(user = user).exists():
            status = "Organizer"
        else:
            status = "Attendee"
            
        try:
            profile_user = get_object_or_404(AttendeeUser, username = user.username)
        except AttendeeUser.DoesNotExist:
            return Response({"error": "This user does not exist."}, status = status.HTTP_403_FORBIDDEN)
        
        profile_data = {
            "id": profile_user.id,
            "username" : profile_user.username,
            "firstname": profile_user.first_name,
            "lastname": profile_user.last_name,
            "birth_date": profile_user.birth_date,
            "phonenumber": profile_user.phone_number,
            "status": status,
        }
        return profile_data