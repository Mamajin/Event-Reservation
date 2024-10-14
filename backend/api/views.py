from ninja import Router, Schema, NinjaAPI, Field
from django.contrib.auth.models import User
from api.models import Organizer, Event, Attendee, Ticket
from ninja import ModelSchema
from django.contrib.auth.hashers import make_password
from pydantic import field_validator
from pydantic import BaseModel

api = NinjaAPI(version = '2.0.0')
router = Router()

# User Registration Schema
class UserSchema(BaseModel):
    username: str
    password: str
    password2: str

    @field_validator('password2')
    def check_passwords_match(cls, password2, values):
        if 'password' in values and values['password'] != password2:
            raise ValueError("Passwords do not match")
        return password2

# Other Schemas
class OrganizerSchema(ModelSchema):
    class Meta:
        model = Organizer
        fields = '__all__'

class EventSchema(ModelSchema):
    class Meta:
        model = Event
        fields = '__all__'

class AttendeeSchema(ModelSchema):
    class Meta:
        model = Attendee
        fields = '__all__'

class TicketSchema(ModelSchema):
    class Meta:
        model = Ticket
        fields = '__all__'

# User API Endpoints
class UserAPI:
    
    
    @router.get("/register", response=UserSchema)
    def show_user_form(self, request):
        return UserSchema.schema()
    
    @router.post("/register", response=UserSchema)
    def create_form(self, request, user: UserSchema):
        if user.password != user.password2:
            return {"error": "Passwords do not match"}, 400  # Returning a proper error message
        
        hashed_password = make_password(user.password)
        user_instance = User.objects.create(username=user.username, password=hashed_password)
        
        # Optionally, you could return more user details
        return {
            "username": user_instance.username,
            "message": "User created successfully."
        }

# Add router to the API
api.add_router("/api/", router)
