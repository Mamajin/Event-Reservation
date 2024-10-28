from django.db import models
from django.utils import timezone


class Session(models.Model):
    """
    Enhanced Session model for managing event sessions with additional features
    for scheduling, capacity management, and speaker information.
    """

    SESSION_TYPE_CHOICES = [
        ('POLLS', 'Polls'),
        ('COMMENT', 'Comment'),
        ('FEEDBACK', 'Feedback'),
    ]

    # Basic Information
    session_name = models.CharField(max_length=255)
    event = models.ForeignKey('Event', related_name='sessions', on_delete=models.CASCADE)
    session_type = models.CharField(
        max_length=20,
        choices=SESSION_TYPE_CHOICES,
        default='PRESENTATION'
    )

    # Timing
    event_create_date = models.DateTimeField('Session Created At', default=timezone.now)
    start_date_event = models.DateTimeField('Session Start Date', null=False, blank=False)
    end_date_event = models.DateTimeField('Session End Date', null=False, blank=False)
    start_date_register = models.DateTimeField('Registration Start Date', default=timezone.now)
    end_date_register = models.DateTimeField('Registration End Date', null=False, blank=False)

    # System Fields
    created_at = models.DateTimeField('Created At', default=timezone.now)
    updated_at = models.DateTimeField('Updated At', auto_now=True)
    

    def __str__(self):
        return f"{self.session_name} - {self.event.event_name}"

