from ninja import Router, NinjaAPI, ModelSchema
from faker import Faker
import datetime
from typing import List
from api.models import Organizer, Event, Ticket, AttendeeUser
from django.utils import timezone
from django.contrib.auth.models import User
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404

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

class TicketSchema(ModelSchema):
    class Config:
        model = Ticket
        model_fields = '__all__'

    
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

@router.post("/create/fake_ticket/", response=TicketSchema)
def create_fake_ticket(request):
    """
    Creates a fake ticket for testing.
    """
    # Create or get a mock attendee user
    user_data = {
        'username': fake.user_name(),
        'email': fake.email(),
        'password': fake.password(),
    }
    user, _ = AttendeeUser.objects.get_or_create(
        username=user_data['username'],
        defaults={'email': user_data['email'], 'password': user_data['password']}
    )

    # Create or get a mock event
    event_data = {
        'event_name': fake.catch_phrase(),
        'event_create_date': fake.date_time_this_year(),
        'start_date_event': fake.future_datetime(end_date="+30d"),
        'end_date_event': fake.future_datetime(end_date="+60d"),
        'start_date_register': fake.date_time_this_year() - datetime.timedelta(days=5),
        'end_date_register': fake.date_time_this_year(),
        'description': fake.text(max_nb_chars=200),
        'max_attendee': fake.random_int(min=10, max=500),
    }

    # Retrieve an organizer or create one
    organizer = Organizer.objects.first()
    if not organizer:
        organizer_user = User.objects.create(
            username=fake.user_name(), 
            email=fake.email(), 
            password=fake.password()
        )
        organizer = Organizer.objects.create(
            user=organizer_user,
            organizer_name=fake.company(),
            email=organizer_user.email
        )

    event, _ = Event.objects.get_or_create(
        organizer=organizer,
        defaults=event_data
    )

    # Create the ticket for the attendee
    ticket = Ticket.objects.create(
        event=event,
        attendee=user
    )

    return ticket


@router.get('event/{user_id}', response=List[TicketSchema])
def list_my_event(request, user_id: int):
    """
    Lists all tickets for a given user.
    """
    user = get_object_or_404(AttendeeUser, id=user_id)
    return user.ticket_set.all()


@router.post('event/{event_id}/reserve', response=TicketSchema)
def event_reserve(request, event_id: int):
    """
    Reserves a ticket for a user for a specific event.
    """
    user_id = request.user.id
    event = get_object_or_404(Event, id=event_id)
    user = get_object_or_404(AttendeeUser, id=user_id)
    ticket = Ticket.objects.create(event=event, attendee=user)
    return ticket


@router.delete('delete-event/{ticket_id}')
def delete_ticket(request, ticket_id: int):
    """
    Cancels a ticket by ID for the authenticated user.
    """
    user = request.user
    try:
        ticket = user.ticket_set.get(id=ticket_id)
        ticket.delete()
        return {"success": f"Ticket with ID {ticket_id} has been canceled."}
    except Ticket.DoesNotExist:
        return {"error": f"Ticket with ID {ticket_id} does not exist."}
    
stub_api.add_router("/mock_api/", router)
