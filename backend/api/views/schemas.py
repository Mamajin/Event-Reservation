from .modules import *


class EventCategory(str, Enum):
    CONFERENCE = 'CONFERENCE'
    WORKSHOP = 'WORKSHOP'
    SEMINAR = 'SEMINAR'
    NETWORKING = 'NETWORKING'
    CONCERT = 'CONCERT'
    SPORTS = 'SPORTS'
    OTHER = 'OTHER'
    

class OrganizerType(str, Enum):
    INDIVIDUAL = 'INDIVIDUAL'
    COMPANY = 'COMPANY'
    NONPROFIT = 'NONPROFIT'
    EDUCATIONAL = 'EDUCATIONAL'
    GOVERNMENT = 'GOVERNMENT'
    
    
class DressCode(str, Enum):
    CASUAL = 'CASUAL'
    SMART_CASUAL = 'SMART_CASUAL'
    BUSINESS_CASUAL = 'BUSINESS_CASUAL'
    SEMI_FORMAL = 'SEMI_FORMAL'
    FORMAL = 'FORMAL'
    BLACK_TIE = 'BLACK_TIE'
    WHITE_TIE = 'WHITE_TIE'
    THEMED = 'THEMED'
    OUTDOOR_BEACH_CASUAL = 'OUTDOOR_BEACH_CASUAL'
    

# Schema for Organizer
class OrganizerSchema(Schema):
    organizer_name: Optional[str]
    email: Optional[EmailStr]
    organization_type: Optional[OrganizerType]


class OrganizerResponseSchema(Schema):
    id: int
    organizer_name: str
    email: EmailStr
    organization_type: OrganizerType
    is_verified: bool


class ErrorResponseSchema(Schema):
    error: str
    
    
class EventInputSchema(ModelSchema):
    category : EventCategory
    dress_code : DressCode

    # not include Organizer Information
    class Meta:
        model = Event
        exclude = ('organizer', 'id', 'status_registeration','tags','status')
    
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


class EventResponseSchema(ModelSchema):
    # Include Organizer information
    category : EventCategory
    dress_code : DressCode
    organizer : OrganizerResponseSchema
    class Meta:
        model = Event
        fields = '__all__'
 
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
        )

    
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
    

class UserResponseSchema(Schema):
    id: int
    username: str
    first_name: str  
    last_name: str   
    birth_date: date 
    phone_number: str  
    email: EmailStr  
    status: str
    address : str
    latitude : Decimal
    longitude: Decimal
    company : str
    facebook_profile : str
    instagram_handle : str
    nationality : str
    attended_events_count: int
    cancelled_events_count : int
    created_at : datetime
    updated_at : datetime
    

# Schema for Ticket
class TicketSchema(Schema):
    ticket_number: str
    event_id: int
    fullname: str
    register_date: datetime
    status: Optional[str] = None
    

class TicketResponseSchema(Schema):
    id: int
    ticket_number: str
    event_id: int
    fullname: str
    register_date: datetime
    status: Optional[str] = None
    created_at: datetime
    updated_at: datetime
        
        
class SessionSchema(Schema):
    session_name: str
    session_type: str
    start_date_event: datetime
    end_date_event: datetime
    start_date_register: Optional[datetime]
    end_date_register: datetime
    description: str
    max_attendee: int


class SessionResponseSchema(Schema):
    id: int
    session_name: str
    event_id: int
    session_type: str
    event_create_date: datetime
    start_date_event: datetime
    end_date_event: datetime
    start_date_register: Optional[datetime]
    end_date_register: datetime
    description: str
    max_attendee: int
    

class FileUploadResponseSchema(Schema):
    file_url: str
    message: str = "Upload successful"
    file_name: str
    uploaded_at: datetime


class ImageUploadSchema(Schema):
    file_url: str
    original_name: str
    file_size: int
    content_type: str

    
class ProfileImageUpdateSchema(Schema):
    profile_picture_url: Optional[str]
    updated_at: datetime


class EventImageUpdateSchema(Schema):
    event_image_url: Optional[str]
    updated_at: datetime
    