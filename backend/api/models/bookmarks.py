from django.db import models
from .event import Event
from .user import AttendeeUser
from django.utils import timezone


class BookmarkManager(models.Manager):
    def has_user_bookmarked(self, event, user):
        """_summary_

        Args:
            event (_type_): _description_
            user (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.filter(event=event, attendee=user).exists()


class Bookmarks(models.Model):
    event = models.ForeignKey(Event, on_delete= models.CASCADE)
    attendee = models.ForeignKey(AttendeeUser, on_delete= models.CASCADE)
    bookmark_at = models.DateTimeField('Bookmark at', default = timezone.now)
    
    
    def __str__(self):
        return f"Attendee : {self.attendee.first_name}, Event : {self.event.event_name}"
