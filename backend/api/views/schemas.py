
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
    
    
class EventVisibility(str, Enum):
    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'
    
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
    logo: Optional[str]
    is_verified: bool
    

class EmailVerificationSchema(Schema):
    token: str


class EmailVerificationResponseSchema(Schema):
    message: str
    verified: bool


class ErrorResponseSchema(Schema):
    error: str
    
    
class EventInputSchema(ModelSchema):
    category : EventCategory
    dress_code : DressCode
    visibility: EventVisibility = EventVisibility.PUBLIC
    allowed_email_domains: Optional[str] = None
    class Meta:
        model = Event
        exclude = ('organizer', 'id', 'status_registeration','tags','status', 'event_image')
    
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


class EventEngagementSchema(Schema):
    total_likes: int
    total_bookmarks: int
    
    
class UserEngagementSchema(Schema):
    is_liked: bool
    is_bookmarked: bool
    

class EventResponseSchema(ModelSchema):
    category : EventCategory
    dress_code : DressCode
    visibility: EventVisibility
    organizer : OrganizerResponseSchema
    engagement: Optional[Dict] = None
    user_engaged: Optional[Dict] = None
    
    @classmethod
    def resolve_engagement(cls, event: Event) -> Dict:
        """
        Resolve engagement information for the event.

        Args:
            event (Optional[Event]): The event for which engagement data is being retrieved.
            user (Optional[AttendeeUser]): The user for whom the engagement data is resolved.

        Returns:
            Dict: Engagement data including total likes, total bookmarks, and user's like status.
        """
        return EventEngagementSchema(
            total_likes=event.like_count,
            total_bookmarks=event.bookmark_count,
        ).dict()
        
    @classmethod
    def resolve_user_engagement(cls, event: Event, user: Optional[AttendeeUser]) -> Dict:
        """
        
        """
        if not user.is_authenticated:
            return UserEngagementSchema(
            is_liked=False,
            is_bookmarked=False
        ).dict()
            
        return UserEngagementSchema(
            is_liked=event.likes.has_user_liked(event, user),
            is_bookmarked=Bookmarks.objects.filter(event=event, attendee=user).exists()
        ).dict()
    
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
            "profile_picture"
        )
        
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
    
    
class OrganizerUpdateSchema(Schema):
    organizer_name: Optional[str] =Field(None)
    email: Optional[EmailStr]= ""
    organization_type: Optional[OrganizerType] = "INDIVIDUAL"
    

class EventUpdateSchema(Schema):
    event_name: Optional[str] = None
    event_create_date: Optional[datetime] = None
    start_date_event: Optional[datetime] = None
    end_date_event: Optional[datetime] = None
    start_date_register: Optional[datetime] = None
    end_date_register: Optional[datetime] = None
    description: Optional[str] = None
    max_attendee: Optional[int] = 0
    address: Optional[str] = None
    is_free: Optional[bool] = True
    ticket_price: Optional[Decimal] = Decimal('0.00')
    expected_price: Optional[Decimal] = Decimal('0.00')
    is_online: Optional[bool] = False
    meeting_link: Optional[str] = None
    category: Optional[str] = 'OTHER'
    visibility: Optional[str] = 'PUBLIC'
    allowed_email_domains: Optional[str] = None
    detailed_description: Optional[str] = None
    dress_code: Optional[str] = 'CASUAL'
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    website_url: Optional[str] = None
    facebook_url: Optional[str] = None
    twitter_url: Optional[str] = None
    instagram_url: Optional[str] = None
    min_age_requirement: Optional[int] = 0
    terms_and_conditions: Optional[str] = None
    
    
    


    
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
    
    
class UserProfileSchema(Schema):
    id: int
    username: str
    profile_picture: Optional[str]
    

class CommentSchema(Schema):
    parent_id: Optional[int] = None
    content: str

    
class CommentResponseSchema(Schema):
    id: int
    user: UserProfileSchema
    content: str
    created_at: datetime
    status: str
    reactions: List[Dict] = []
    replies: List['CommentResponseSchema'] = []
