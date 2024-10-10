from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_create_date = models.DateTimeField('Event Created At', default= timezone.now)
    start_date_event = models.DateTimeField('Event Start Date', null = False, blank= False)
    end_date_event = models.DateTimeField('Event End Date', null= False, blank = True)
    start_date_register = models.DateTimeField('Registration Start Date', default=timezone.now)
    end_date_register = models.DateTimeField('Registration End Date', null = False , blank= False)
    description = models.TextField(max_length=400)
    
    
    
class Attendee(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    event_list = models.ManyToManyField(Event, through= 'Ticket')
    
    
# Create your models here.
class Organizer(models.Model):
    """
    An Organizer model class contains organizer attributes
    and a method...
    """
    organizer_name = models.CharField(max_length=100)
    email = models.EmailField()
    event_list = models.ManyToManyField(Event, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.user.first_name
