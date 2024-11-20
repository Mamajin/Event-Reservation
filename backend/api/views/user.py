from api.views.schemas.user_schema import *
from api.views.schemas.other_schema import *
from .modules import *
from .strategy.user_strategy import UserStrategy



@api_controller("/users/", tags = ["Users"])
class UserAPI:
    """
    Controller for user-related operations.
    """
    @route.post('/register', response={201: UserSchema, 400: ErrorResponseSchema})
    def create_user(self,request, form: UserSchema = Form(...)):
        """
        Create a new user and return the created user object.

        Args:
            request: The HTTP request object.
            form (UserSchema): The user registration data.

        Returns:
            UserSchema: The created user object on successful registration.
        """
        strategy : UserStrategy = UserStrategy.get_strategy('user_register')
        return strategy.execute(form)
    
    @route.post('/logout', response={200: dict})
    def logout(self,request):
        """
        Logs out the current user.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A success message with a 200 status code.
        """
        strategy : UserStrategy = UserStrategy.get_strategy('user_logout')
        return strategy.execute(request)

    @route.post('/auth/google', response=AuthResponseSchema)
    def google_auth(self,request, data: GoogleAuthSchema):
        """
        Authenticate a user via Google OAuth2 and retrieve access and refresh tokens.

        Args:
            request: The request object.
            data (GoogleAuthSchema): Google authentication token data.

        Returns:
            Response: A response containing user details and tokens on successful authentication.
        """
        strategy : UserStrategy = UserStrategy.get_strategy('user_google_login')
        return strategy.execute(request, data)
                    
    
    @route.post('/login', response = LoginResponseSchema)
    def login(self,request, form: LoginSchema = Form(...)):
        """
        Log in a user with username and password, returning access and refresh tokens.

        Args:
            request: The request object.
            form (LoginSchema): The login details (username and password).

        Returns:
            Response: A response containing tokens and user details upon successful login.
        """
        strategy : UserStrategy = UserStrategy.get_strategy('user_login')
        return strategy.execute(request, form)

    @route.get('/profile', response=UserResponseSchema, auth=JWTAuth())
    def view_profile(self,request):
        """
        Retrieve the profile of the currently logged-in user.

        Returns:
            UserResponseSchema: The profile details of the user.
        """
        strategy : UserStrategy = UserStrategy.get_strategy('user_view_profile')
        return strategy.execute(request)

    @route.patch('/edit-profile/{user_id}/', response=UserupdateSchema, auth=JWTAuth())
    def edit_profile(self,request, user_id: int, new_data: UserupdateSchema):
        """
        Update the profile information of a user by user ID.

        Args:
            request: The request object.
            user_id (int): The ID of the user to be updated.
            new_data (UserResponseSchema): New profile data for the user.

        Returns:
            UserResponseSchema: Updated user profile details.
        """
        strategy : UserStrategy = UserStrategy.get_strategy('user_edit_profile')
        return strategy.execute(user_id, new_data)

    @route.delete('delete/', auth=JWTAuth())
    def delete_profile(self,request):
        """
        Delete a user profile by user ID.

        Args:
            request: The request object.
            user_id (int): The ID of the user to delete.

        Returns:
            Response: Success message upon successful deletion.
        """
        strategy : UserStrategy = UserStrategy.get_strategy('user_delete_account')
        return strategy.execute(request)
    @route.post('/{user_id}/upload/profile-picture/', response={200: FileUploadResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())
    def upload_profile_picture(self,request: HttpRequest, user_id: int, profile_picture: UploadedFile = File(...)):
        """
        Upload a profile picture for the specified user.

        Args:
            request (HttpRequest): The request object containing the file.
            user_id (int): The ID of the user for whom the profile picture is uploaded.
            profile_picture (UploadedFile): The uploaded profile picture file.

        Returns:
            Response: URL and details of the uploaded profile picture.
        """
        strategy: UserStrategy = UserStrategy.get_strategy('user_upload_picture')
        return strategy.execute(request, profile_picture)
        
    @route.get('/verify-email/{user_id}/{token}', response={200: EmailVerificationResponseSchema, 400: ErrorResponseSchema})
    def verify_email(self,request, user_id: str, token: str):
        """
        Verify the email address of the user with the specified user ID and verification token.

        Args:
            request: The request object.
            user_id (str): The ID of the user whose email is to be verified.
            token (str): The verification token sent to the user's email address.

        Returns:
            EmailVerificationResponseSchema: Verification success message or error response.
        """
        
        strategy: UserStrategy = UserStrategy.get_strategy('user_verify_email')
        return strategy.execute(user_id, token)

    @route.post('/resend-verification', response={200: EmailVerificationResponseSchema, 400: ErrorResponseSchema})
    def resend_verification(self,request, email: str):
        """
        Resend the verification email to the specified email address.

        Args:
            request: The request object.
            email (str): The email address to which the verification email is to be resent.

        Returns:
            EmailVerificationResponseSchema: Verification success message or error response.
        """
        
        strategy : UserStrategy = UserStrategy.get_strategy('user_resend_verification')
        return strategy.execute(email)
