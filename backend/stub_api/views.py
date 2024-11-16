from ninja import Router, NinjaAPI, ModelSchema
from faker import Faker
import datetime
from typing import List
from api.models import Organizer, Event
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

stub_api = NinjaAPI(version='1.0.0')
router = Router()
fake = Faker()




 # Adjust these fields based on your Organizer model
 
class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['id', 'username', 'password','email'] 
        
 
class OrganizerSchema(ModelSchema):
    user : UserSchema
    
    class Meta:
        model = Organizer
        fields = ['user', 'organizer_name', 'email']


class EventSchema(ModelSchema):
    organizer: OrganizerSchema
    class Meta:
        model = Event
        fields = [
            'event_name',
            'organizer',
            'event_create_date',
            'start_date_event',
            'end_date_event',
            'start_date_register',
            'end_date_register',
            'description',
            'max_attendee',
        ]
        # Optional: You can also define nested schemas if you need more detail for the organizer


    
@router.get("/event/", response=List[EventSchema])  
def show_event(request):
    # Create a sample organizer to associate with events
    
    organizer = Organizer.objects.first()
    # print(organizer.id, "win")# Assuming you have at least one organizer in your DB
    events = [
        EventSchema(
            event_name=fake.company(),
            organizer= OrganizerSchema.from_orm(organizer), 
            start_date_event=fake.date_time_this_year(),
            end_date_event=fake.date_time_this_year() + datetime.timedelta(days=1),  # Ensure it ends after it starts
            start_date_register=fake.date_time_this_year() - datetime.timedelta(days=5),  # Example for registration start
            end_date_register=fake.date_time_this_year(),  # Registration ends when the event starts
            max_attendee=fake.random_int(min=10, max=500),
            description=fake.text(max_nb_chars=200)
        )
    ]
    return events 



@router.get("/event_actual/", response= List[EventSchema])
def show_all_event(request):
    return Event.objects.all()

    


@router.post("/create/event/", response=EventSchema)
def create_event(request):
    # Generate mock user data
    user_data = {
        'username': fake.user_name(),
        'email': fake.email(),
        'password': fake.password() 
    }

    # Create or get the user instance
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'password': user_data['password'], 
        }
    )

    # Generate mock organizer data
    organizer_data = {
        'organizer_name': fake.company(),
        'email': fake.email()
    }

    # Create or retrieve the organizer instance
    organizer, _ = Organizer.objects.get_or_create(
        user=user,
        defaults={
            'organizer_name': organizer_data['organizer_name'],
            'email': organizer_data['email'],
        }
    )

    event_data = {
        'event_name': fake.catch_phrase(),
        'event_create_date': fake.date_time_this_year(),
        'start_date_event': fake.date_time_this_year(),
        'end_date_event': fake.date_time_this_year() + datetime.timedelta(days=1),
        'start_date_register': fake.date_time_this_year() - datetime.timedelta(days=5),
        'end_date_register': fake.date_time_this_year(),
        'description': fake.text(max_nb_chars=200),
        'max_attendee': fake.random_int(min=10, max=500)
    }

    # Create the event instance with the organizer
    event = Event.objects.create(
        organizer=organizer,
        **event_data  
    )
    
    return event
    
    
stub_api.add_router("/mock_api/", router)
    
    

    