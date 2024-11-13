from django.db import models
from django.utils import timezone
from api.models.event import Event
from api.models.user import AttendeeUser


class LikeManager(models.Manager):
    def has_user_liked(self, event, user):
        """
        Check if the user has liked the specified event.
        
        Args:
            event (Event): The event to check.
            user (AttendeeUser): The user to check.

        Returns:
            bool: True if the user has liked the event, False otherwise.
        """
        return self.filter(event=event, user=user).exists()


class Like(models.Model):
    """
    Model to represent a like on an event by a user.

    Fields:
        event (ForeignKey): The event that was liked.
        user (ForeignKey): The user who liked the event.
        liked_at (DateTimeField): The time the event was liked.
    """
    event = models.ForeignKey(Event, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(AttendeeUser, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    objects = LikeManager()

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} liked {self.event.event_name} at {self.liked_at}"

    # @staticmethod
    # def toggle_like(event, user):
    #     """
    #     Toggle the like status for an event by a user. If the user has already liked the event,
    #     it will unlike it; otherwise, it will add a like.

    #     Args:
    #         event (Event): The event to like or unlike.
    #         user (AttendeeUser): The user performing the action.

    #     Returns:
    #         str: A message indicating whether the event was liked or unliked.
    #     """
    #     like, created = Like.objects.get_or_create(event=event, user=user)
    #     if not created:
    #         like.delete()
    #         return "Unliked the event."
    #     return "Liked the event."
