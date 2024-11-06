from django.db import models
from api.models.user import AttendeeUser
from api.models.event import Event

class Comment(models.Model):
    """Model for session comments with threading and moderation capabilities"""

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Review'
        APPROVED = 'APPROVED', 'Approved'
        HIDDEN = 'HIDDEN', 'Hidden'
        FLAGGED = 'FLAGGED', 'Flagged'

    # Relationships
    event = models.ForeignKey(Event, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(AttendeeUser, related_name='session_comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    
    content = models.TextField()
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.APPROVED
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.session.session_name}"
    
    
class CommentReaction(models.Model):
    """Model for comment reactions (likes, etc.)"""

    REACTION_CHOICES = [
        ('LIKE', '👍'),
        ('LOVE', '❤️'),
        ('LAUGH', '😄'),
    ]

    comment = models.ForeignKey(Comment, related_name='reactions', on_delete=models.CASCADE)
    user = models.ForeignKey(AttendeeUser, related_name='comment_reactions', on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['comment', 'user', 'reaction_type']
        