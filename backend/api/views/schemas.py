from .modules import *


class EventCategory(str, Enum):
    CONFERENCE = 'CONFERENCE'
    WORKSHOP = 'WORKSHOP'
    SEMINAR = 'SEMINAR'
    NETWORKING = 'NETWORKING'
    CONCERT = 'CONCERT'
    SPORTS = 'SPORTS'
    OTHER = 'OTHER'

# Schema for Organizer
class OrganizerSchema(Schema):
    organizer_name: Optional[str]
    email: Optional[str]


class OrganizerResponseSchema(Schema):
    id: int
    organizer_name: str
    email: str
    organizer_type: str
    is_verified: str


class ErrorResponseSchema(Schema):
    error: str

# Schemas for Event
class EventSchema(ModelSchema):
    event_name: str
    organizer_id: int 
    event_create_date: datetime
    start_date_event: datetime
    end_date_event: datetime
    start_date_register: datetime
    end_date_register: datetime
    description: str
    max_attendee: int
    event_image: Optional[str]
    venue_name: Optional[str]
    street_address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    is_free: bool
    ticket_price: Decimal
    expected_price: Decimal 
    is_online: bool  
    category: EventCategory
    tags: Optional[str] 
    detailed_description: Optional[str]
    status: str 
    contact_email: Optional[str]
    contact_phone: Optional[str]
    website_url: Optional[str] 
    facebook_url: Optional[str] 
    twitter_url: Optional[str]  
    instagram_url: Optional[str]
    min_age_requirement: Optional[int]
    terms_and_conditions: Optional[str] 
    updated_at: datetime  
    

class EventResponseSchema(Schema):
    id: int
    event_name: str
    organizer_id: int 
    event_create_date: datetime
    start_date_event: datetime
    end_date_event: datetime
    start_date_register: datetime
    end_date_register: datetime
    description: str
    max_attendee: int
    event_image: Optional[str]
    venue_name: Optional[str]
    street_address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    is_free: bool
    ticket_price: Decimal
    expected_price: Decimal 
    is_online: bool  
    category: EventCategory
    tags: Optional[str] 
    detailed_description: Optional[str]
    status: str 
    contact_email: Optional[EmailStr]
    contact_phone: Optional[str]
    website_url: Optional[HttpUrl] 
    facebook_url: Optional[str] 
    twitter_url: Optional[str]  
    instagram_url: Optional[str]
    min_age_requirement: Optional[int]
    terms_and_conditions: Optional[str] 
    updated_at: datetime               
 
# Schema for User                
class UserSchema(Schema):
    username: str
    password: str
    password2: str
    first_name: str
    last_name : str
    birth_date: date
    phone_number: str
    email: str

    
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
    firstname: str
    lastname: str
    birth_date: date 
    phonenumber: str
    status: str

# Schema for Ticket
class TicketSchema(Schema):
    ticket_number: str
    event: str
    attendee: str
    register_date: datetime
    status: Optional[str]
    

class TicketResponseSchema(Schema):
    id: int
    ticket_number: str
    event: str
    attendee: str
    register_date: datetime
    status: Optional[str]
        
        
class SessionSchema(Schema):
    session_name: str
    event_name: str
    session_type: str
    start_date_event: datetime
    end_date_event: datetime
    start_date_register: Optional[datetime]
    end_date_register: datetime
    description: str
    max_attendee: int
    session_type: str


class SessionResponseSchema(Schema):
    id: int
    session_name: str
    event_name: str
    event_create_date: datetime
    start_date_event: datetime
    end_date_event: datetime
    start_date_register: Optional[datetime]
    end_date_register: datetime
    description: str
    max_attendee: int
    session_type: str
    