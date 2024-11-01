from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Q
from typing import List, Optional
from datetime import datetime, timedelta
from api.models.event import Event

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
    event = models.ForeignKey(Event, related_name='sessions', on_delete=models.CASCADE)
    session_type = models.CharField(
        max_length=20,
        choices=SESSION_TYPE_CHOICES,
        default='POLLS'
    )
    description = models.TextField(blank=True)
    max_attendee = models.PositiveIntegerField(default=0)

    # Timing
    event_create_date = models.DateTimeField('Session Created At', default=timezone.now)
    start_date_event = models.DateTimeField('Session Start Date')
    end_date_event = models.DateTimeField('Session End Date')
    start_date_register = models.DateTimeField('Registration Start Date', default=timezone.now)
    end_date_register = models.DateTimeField('Registration End Date')

    # System Fields
    created_at = models.DateTimeField('Created At', default=timezone.now)
    updated_at = models.DateTimeField('Updated At', auto_now=True)

    class Meta:
        ordering = ['start_date_event']
        indexes = [
            models.Index(fields=['event', 'start_date_event']),
            models.Index(fields=['session_type']),
        ]

    def __str__(self):
        return f"{self.session_name} - {self.event.event_name}"

    def clean(self):
        """Validate session dates and registration dates."""
        if self.start_date_event and self.end_date_event:
            if self.start_date_event >= self.end_date_event:
                raise ValidationError({
                    'start_date_event': 'Session start date must be before end date.'
                })

        if self.start_date_register and self.end_date_register:
            if self.start_date_register >= self.end_date_register:
                raise ValidationError({
                    'start_date_register': 'Registration start date must be before end date.'
                })

        if self.end_date_register and self.start_date_event:
            if self.end_date_register > self.start_date_event:
                raise ValidationError({
                    'end_date_register': 'Registration must end before session starts.'
                })

    def save(self, *args, **kwargs):
        """Override save to perform full validation."""
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_active(self) -> bool:
        """Check if the session is currently active."""
        now = timezone.now()
        return self.start_date_event <= now <= self.end_date_event

    @property
    def is_registration_open(self) -> bool:
        """Check if registration is currently open."""
        now = timezone.now()
        return self.start_date_register <= now <= self.end_date_register

    @property
    def duration(self) -> timedelta:
        """Get session duration."""
        return self.end_date_event - self.start_date_event

    def get_overlapping_sessions(self) -> List['Session']:
        """Find all sessions that overlap with this one."""
        return Session.objects.filter(
            event=self.event
        ).filter(
            Q(start_date_event__lt=self.end_date_event) &
            Q(end_date_event__gt=self.start_date_event)
        ).exclude(id=self.id)

    def has_capacity(self) -> bool:
        """Check if session has remaining capacity."""
        if self.max_attendee == 0:  # 0 means unlimited
            return True
        return self.attendees.count() < self.max_attendee
    
    def get_session_detail(self):
        """Return Session details."""
        return {
            'session_name': self.session_name,
            'event_id': self.event.id,
            'session_type': self.session_type,
            'event_create_date': self.event_create_date,
            'start_date_event': self.start_date_event,
            'end_date_event': self.end_date_event,
            'start_date_register': self.start_date_register,
            'end_date_register': self.end_date_register,
            'description': self.description,
            'max_attendee': self.max_attendee
        }

    @property
    def remaining_capacity(self) -> Optional[int]:
        """Get remaining capacity. Returns None if unlimited."""
        if self.max_attendee == 0:
            return None
        return self.max_attendee - self.attendees.count()

    def __str__(self):
        return f"{self.session_name} - {self.event.event_name}"

