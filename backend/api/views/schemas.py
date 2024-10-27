from .modules import *



# Schema for Organizer
class OrganizerSchema(Schema):
    organizer_name: Optional[str]
    email: Optional[str]


class OrganizerResponseSchema(Schema):
    id: int
    organizer_name: str
    email: str


class ErrorResponseSchema(Schema):
    error: str
    
    
    


# Schemas for Event

class EventSchema(ModelSchema):
    class Meta:
        model = Event
        fields = [
            'event_name',
            'event_create_date',
            'start_date_event',
            'end_date_event',
            'start_date_register',
            'end_date_register',
            'description',
            'max_attendee',
        ]
    

class EventResponseSchema(Schema):
    id: int
    organizer: OrganizerResponseSchema
    event_name: str
    event_create_date: datetime
    start_date_event: datetime
    end_date_event: datetime
    start_date_register: datetime
    end_date_register: datetime
    description: str
    max_attendee: int
                
                
                
 
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
class TicketSchema(ModelSchema):
    class Meta:
        model = Ticket
        fields = ['id','event', 'attendee', 'register_date']