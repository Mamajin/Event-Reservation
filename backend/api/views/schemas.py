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
    has_user_liked: bool
    

class EventResponseSchema(ModelSchema):
    category : EventCategory
    dress_code : DressCode
    visibility: EventVisibility
    organizer : OrganizerResponseSchema
    engagement: Optional[Dict] = None
    
    @classmethod
    def resolve_engagement(cls, event: Event, user: Optional[AttendeeUser]) -> Dict:
        """
        Resolve engagement information for the event.

        Args:
            event (Event): The event for which engagement data is being retrieved.
            user (Optional[AttendeeUser]): The user for whom the engagement data is resolved.

        Returns:
            Dict: Engagement data including total likes, total bookmarks, and user's like status.
        """
        has_user_liked = (
            event.likes.has_user_liked(event=event, user=user)
            if user and user.is_authenticated else False
        )
        return EventEngagementSchema(
            total_likes=event.like_count,  # Example, adjust based on your model
            total_bookmarks=event.bookmark_count,
            has_user_liked=has_user_liked
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
