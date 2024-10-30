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
    # not include Organizer Information
    class Meta:
        model = Event
        exclude = ('organizer', 'id')
    
    
class EventResponseSchema(ModelSchema):
    # Include Organizer information
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

# Schema for Ticket
class TicketSchema(Schema):
    ticket_number: str
    event_id: int
    user_id: int
    register_date: datetime
    status: Optional[str]
    

class TicketResponseSchema(Schema):
    id: int
    ticket_number: str
    event_id: int
    user_id: int
    register_date: datetime
    status: Optional[str]
        
        
class SessionSchema(Schema):
    session_name: str
    event_id: int
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
    event_id: int
    event_create_date: datetime
    start_date_event: datetime
    end_date_event: datetime
    start_date_register: Optional[datetime]
    end_date_register: datetime
    description: str
    max_attendee: int
    session_type: str
    