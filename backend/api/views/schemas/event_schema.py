from api.views.modules import *
from .organizer_schema import OrganizerResponseSchema
from .user_schema import UserEngagementSchema


# Enums for event categories, organizer types, dress codes, and visibility
class EventCategory(str, Enum):
    CONFERENCE = 'CONFERENCE'
    WORKSHOP = 'WORKSHOP'
    SEMINAR = 'SEMINAR'
    NETWORKING = 'NETWORKING'
    CONCERT = 'CONCERT'
    SPORTS = 'SPORTS'
    OTHER = 'OTHER'
    
class EventVisibility(str, Enum):
    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'
    
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
    
# Schema for Event
class EventInputSchema(ModelSchema):
    category : EventCategory
    dress_code : DressCode
    visibility: EventVisibility = EventVisibility.PUBLIC
    allowed_email_domains: Optional[str] = None
    max_attendee: Optional[int] = None
    
    @field_validator("max_attendee", mode="before")
    def validate_max_attendee(cls, value):
        # Convert empty strings or None to None
        if value in (None, ""):
            return None
        # Ensure the value can be parsed as an integer
        try:
            return int(value)
        except ValueError:
            raise ValueError("max_attendee must be a valid integer or null")
    
    class Meta:
        model = Event
        exclude = ('organizer', 'id', 'status_registeration','tags','status', 'event_image','updated_at')     

class EventResponseSchema(ModelSchema):
    category : EventCategory
    dress_code : DressCode
    visibility: EventVisibility
    organizer : OrganizerResponseSchema
    engagement: Optional[Dict] = None
    user_engaged: Optional[Dict] = None
    current_attendees: Optional[int] = 0
    status_registeration: Optional[str] = None
    
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
    def resolve_user_engagement(cls, event: Event, user: Optional[AttendeeUser] = None) -> Dict:
        """
        Resolve user engagement information for the event.

        Args:
            event (Event): The event for which user engagement data is being retrieved.
            user (Optional[AttendeeUser]): The user for whom the engagement data is resolved.

        Returns:
            Dict: User engagement data including the user's like status and bookmark status.
        """
        if user is None or not user.is_authenticated:
            return UserEngagementSchema(
                is_liked=False,
                is_bookmarked=False,
                is_applied=False
            ).dict()
        
        return UserEngagementSchema(
            is_liked=event.likes.has_user_liked(user, event),
            is_bookmarked=Bookmarks.objects.filter(event=event, attendee=user).exists(),
            is_applied=Ticket.objects.filter(event=event, attendee=user).exists(),
        ).dict()
        
    @classmethod
    def set_status_event(cls, event: Event):
        event.set_registeration_status()
        event.set_status_event()
        event.current_attendees = event.current_number_attendee
    
    class Meta:
        model = Event
        fields = '__all__'

class EventUpdateSchema(Schema):
    event_name: Optional[str] = None
    event_create_date: Optional[datetime] = None
    start_date_event: Optional[datetime] = None
    end_date_event: Optional[datetime] = None
    start_date_register: Optional[datetime] = None
    end_date_register: Optional[datetime] = None
    tags : Optional[str] = None
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
    
class EventEngagementSchema(Schema):
    total_likes: int
    total_bookmarks: int