from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Organizer(models.Model):
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
        return self.organizer_name


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
    max_attendee = models.IntegerField(default=0)


    
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
    
    def is_end_date_register_lte_start_date_event(self) -> bool:
        """
        Check if event date is valid. If event end date is before event start date
        then event is not valid.

        Return:
            bool: True if event is valid, False if event is not valid
        """
        return self.end_date_register < self.start_date_event
        
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
    
    
    
class Attendee(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    event_list = models.ManyToManyField(Event, through= 'Ticket')
    
    
    def show_event_registered(self):
        """
        Get all events an attendee has joined

        Return:
            query_set: List of events an attendee has joined
        """
        return self.event_list.all()
    
    
    
    
    def __str__(self) -> str:
        return f"Name: {self.user.username}"
    

    
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete= models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete= models.CASCADE)
    register_date = models.DateTimeField('Date registered', default= timezone.now)
    
    def __str__(self) -> str:
        return f"Event: {self.event.event_name}, Attendee: {self.attendee.user.username}"
        
    def add_event(self, event) -> None:
        """
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



class Ticket(models.Model):
    """
    Represents a ticket that connects an Attendee to an Event. 
    Tracks the date of registration for the event.

    Attributes:
        event (ForeignKey): The event the ticket is for.
        attendee (ForeignKey): The attendee who registered for the event.
        register_date (datetime): The date the attendee registered for the event.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    register_date = models.DateTimeField('Date registered', default=timezone.now)

    def __str__(self) -> str:
        """
        Return a string representation of the Ticket object.
        
        Returns:
            str: A string indicating the event name for the ticket.
        """
        return f"Ticket for {self.event.event_name}"
    
    def cancel_ticket(self) -> None:
        """
        Cancels the ticket by deleting the Ticket instance.
        """
        self.delete()

