from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Organizer(models.Model):
    organizer_name = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return self.organizer_name


class Event(models.Model):
    event_name = models.CharField(max_length=100)
    organizer = models.ForeignKey(Organizer, on_delete= models.CASCADE, related_name = 'events')
    event_create_date = models.DateTimeField('Event Created At', default= timezone.now)
    start_date_event = models.DateTimeField('Event Start Date', null = False, blank= False)
    end_date_event = models.DateTimeField('Event End Date', null= False, blank = True)
    start_date_register = models.DateTimeField('Registration Start Date', default=timezone.now)
    end_date_register = models.DateTimeField('Registration End Date', null = False , blank= False)
    description = models.TextField(max_length=400)
    max_attendee = models.IntegerField(default=0)

    
    @property
    def current_number_attendee(self):
        return self.ticket_set.count()
    
    
    def is_max_attendee(self):
        if self.current_number_attendee == self.max_attendee:
            return True
        return False
    
    def is_event_published(self):
        now = timezone.now()
        return self.event_create_date <= now
    
    def is_end_date_register_lte_start_date_event(self):
        return self.end_date_register < self.start_date_event
        
    def can_register(self):
        now = timezone.now()
        return self.start_date_register <= now < self.end_date_register
    
        
    def __str__(self):
        return f"Event: {self.event_name}"
    
    
    
class Attendee(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    event_list = models.ManyToManyField(Event, through= 'Ticket')
    
    def __str__(self):
        return f"Name: {self.user.username}"
    

    
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete= models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete= models.CASCADE)
    register_date = models.DateTimeField('Date registered', default= timezone.now)
    
    def __str__(self):
        return f"Event: {self.event.event_name}, Attendee: {self.attendee.user.username}"
        

    
    
