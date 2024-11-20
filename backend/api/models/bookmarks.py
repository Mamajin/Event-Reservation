from django.db import models
from .event import Event
from .user import AttendeeUser
from django.utils import timezone


class BookmarkManager(models.Manager):
    def has_user_bookmarked(self, event, user):
        """
        Check if the user has bookmarked the specified event.

        Args:
            event (Event): The event to check.
            user (AttendeeUser): The user to check.

        Returns:
            bool: True if the user has bookmarked the event, False otherwise.
        """
        return self.filter(event=event, attendee=user).exists()


class Bookmarks(models.Model):
    """Model for storing bookmarked events by users. """
    event = models.ForeignKey(Event, on_delete= models.CASCADE)
    attendee = models.ForeignKey(AttendeeUser, on_delete= models.CASCADE)
    bookmark_at = models.DateTimeField('Bookmark at', default = timezone.now)
    
    
    def __str__(self):
        return f"Attendee : {self.attendee.first_name}, Event : {self.event.event_name}"
