from django.db import models
from .event import Event
from .user import AttendeeUser
from django.utils import timezone



class Bookmarks(models.Model):
    event = models.ForeignKey(Event, on_delete= models.CASCADE)
    attendee = models.ForeignKey(AttendeeUser, on_delete= models.CASCADE)
    bookmark_at = models.DateTimeField('Bookmark at', default = timezone.now)
    
    
    def __str__(self):
        return f"Attendee : {self.attendee.first_name}, Event : {self.event.event_name}"
    
    
    
