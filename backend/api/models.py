from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator



class AttendeeUser(AbstractUser):
    first_name = models.CharField(max_length= 100, null = False, blank= False)
    last_name = models.CharField(max_length= 100, null = False , blank = False)
    birth_date = models.DateField('Birth Date', null=False, blank=False)
    phone_number = models.CharField(max_length=50, null = False, blank= False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='attendeeuser_set',  # Change this to your desired name
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='attendeeuser_set',  # Change this to your desired name
        blank=True,
    )
    
    @property
    def age(self):
        today = timezone.now().date()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
            
        return age
    

class Organizer(models.Model):
    user = models.ForeignKey(AttendeeUser, on_delete= models.CASCADE)
    organizer_name = models.CharField(max_length=100)
    email = models.EmailField()

    
    def show_event(self):
        """
        Returns all events an Organizer has ever organized both active and closed
        events

        Returns:
            query_set: List of events an organizer have organized
        """
        return Organizer.event_set.all()
    
    
    def __str__(self) -> str:
        return f"Organizer name: {self.organizer_name}"


class Event(models.Model):
    """
    Represents an event with a name, creation date, start/end dates, 
    registration period, and a description.

    Attributes:
        event_name (str): The name of the event.
        event_create_date (datetime): The date and time the event was created.
        start_date_event (datetime): The date and time the event starts.
        end_date_event (datetime): The date and time the event ends.
        start_date_register (datetime): The start date for registration.
        end_date_register (datetime): The end date for registration.
        description (str): A brief description of the event (up to 400 characters).
    """
    event_name = models.CharField(max_length=100)
    organizer = models.ForeignKey(Organizer, on_delete= models.CASCADE, related_name = 'events')
    event_create_date = models.DateTimeField('Event Created At', default= timezone.now)
    start_date_event = models.DateTimeField('Event Start Date', null = False, blank= False)
    end_date_event = models.DateTimeField('Event End Date', null= False, blank = True)
    start_date_register = models.DateTimeField('Registration Start Date', default=timezone.now)
    end_date_register = models.DateTimeField('Registration End Date', null=False, blank=False)
    description = models.TextField(max_length=400)
    max_attendee = models.IntegerField(default=0, validators = [MinValueValidator(0)])

    
    @property
    def current_number_attendee(self):
        return self.ticket_set.count()
    
    def get_event_status(self) -> str:
        """
        Get current event Status

        Returns:
            str: String of the current status of the event
        """
        now = timezone.now()
        if now < self.start_date_event:
            return "Upcoming"
        elif self.start_date_event <= now <= self.end_date_event:
            return "Ongoing"
        else:
            return "Finished"

    def available_spot(self) -> int:
        """
        Get availble spots left in an event

        Return:
            int: Number of slots available for the event
        """
        return self.max_attendee - self.current_number_attendee
    
    
    def is_max_attendee(self) -> bool:
        """
        Check if event is slots are full

        Return:
            bool: True if event is full on slots, False if event is not full
        """
        if self.current_number_attendee == self.max_attendee:
            return True
        return False
    
    def is_event_published(self) -> bool:
        """
        Check if event is published

        Return:
            bool: True if event is published  if not return False
        """
        now = timezone.now()
        return self.event_create_date <= now
    
    def is_valid_date(self) -> bool:
        return self.start_date_register <= self.end_date_register <= self.start_date_event <= self.end_date_event
        
    def can_register(self) -> bool:
        """
        Check if registered within register period.

        Return:
            bool: True if can register, False if cannot register
        """
        now = timezone.now()
        return self.start_date_register <= now < self.end_date_register
        
    def __str__(self) -> str:
        return f"Event: {self.event_name}"
    
    
    
    
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete= models.CASCADE)
    attendee = models.ForeignKey(AttendeeUser, on_delete= models.CASCADE)
    register_date = models.DateTimeField('Date registered', default= timezone.now)
    
        
    def add_event(self, event) -> None:
        """
        Adds an event to the attendee's event list.

        Args:
            event (Event): The event to be added.
        """
        self.event_list.add(event)

    def remove_event(self, event) -> None:
        """
        Removes an event from the organizer's event list.

        Args:
            event (Event): The event to be removed.
        """
        self.event_list.remove(event)

    def cancel_ticket(self) -> None:
        """
        Cancels the ticket by deleting the Ticket instance.
        """
        self.delete()
        
    def is_organizer_join_own_event(self):
        if Organizer.objects.filter(user = self.attendee).exists():
            organizer = Organizer.objects.get(user = self.attendee)
            if self.event.organizer == organizer:
                return True
        return False
    
    def is_user_register_the_same_event(self):
        if Ticket.objects.filter(attendee = self.attendee, event = self.event).exists():
            return True
        return False
        
    def __str__(self) -> str:
        return f"Event: {self.event.event_name}, Attendee: {self.attendee.first_name}"
    