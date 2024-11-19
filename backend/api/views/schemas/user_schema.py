from api.views.modules import *


class AuthResponseSchema(Schema):
    access_token: str
    refresh_token : str
    status : str
    first_name : str
    last_name : str
    picture : str
    email : str
    
class GoogleAuthSchema(Schema):
    token: str

# Schema for Login
class LoginSchema(Schema):
    username: str
    password: str    

class LoginResponseSchema(Schema):
    id : int
    username: str
    password: str
    access_token: str
    refresh_token: str
    status : str
    image_url: str = None
    
# Schema for User Engagement
class UserEngagementSchema(Schema):
    is_liked: bool
    is_bookmarked: bool
    is_applied: bool
    
# Schema for User Profile
class UserProfileSchema(Schema):
    id: int
    username: str
    profile_picture: Optional[str]
 
# Schema for User                
class UserSchema(ModelSchema):
    password2: Optional[str] = None
    class Meta:
        model = AttendeeUser
        fields = (
            "username",
            "password",          
            "email",             
            "first_name",        
            "last_name",        
            "birth_date",       
            "phone_number",
            "profile_picture"
        )

class UserResponseSchema(Schema):
    id: int
    username: str
    first_name: str  
    last_name: str   
    birth_date: Optional[date] = None
    phone_number: Optional[str]  = None
    email: EmailStr  
    status: str
    address : str
    latitude: Optional[Decimal] = 0.00 
    longitude: Optional[Decimal] = 0.00 
    profile_picture: Optional[str]  # Ensure this is also 
    company : str
    facebook_profile : str
    instagram_handle : str
    nationality : str
    attended_events_count: int
    cancelled_events_count : int
    created_at : datetime
    updated_at : datetime
    
class UserupdateSchema(Schema):
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = ""
    birth_date: Optional[date] = Field(None)
    phone_number: Optional[str] = Field(None)
    email: Optional[str]  = ""
    address: Optional[str] = Field(None)
    nationality: Optional[str] = Field(None)
    facebook_profile: Optional[str] = Field(None)
    instagram_handle: Optional[str] = Field(None)
    company: Optional[str] = Field(None)
    profile_picture: Optional[str] = Field(None)