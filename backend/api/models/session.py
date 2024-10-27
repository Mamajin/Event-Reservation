from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal


class Session(models.Model):
    """
    Enhanced Session model for managing event sessions with additional features
    for scheduling, capacity management, and speaker information.
    """

    SESSION_TYPE_CHOICES = [
        ('PRESENTATION', 'Presentation'),
        ('WORKSHOP', 'Workshop'),
        ('PANEL', 'Panel Discussion'),
        ('NETWORKING', 'Networking'),
        ('BREAKOUT', 'Breakout Session'),
        ('KEYNOTE', 'Keynote'),
        ('TRAINING', 'Training'),
    ]

    DIFFICULTY_LEVEL_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
        ('ALL_LEVELS', 'All Levels'),
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

    # Content Information
    description = models.TextField(max_length=400)
    detailed_description = models.TextField(blank=True)
    learning_objectives = models.TextField(blank=True)
    prerequisites = models.TextField(blank=True)
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_LEVEL_CHOICES,
        default='ALL_LEVELS'
    )

    # Capacity Management
    max_attendee = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    min_attendee = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    waitlist_limit = models.PositiveIntegerField(default=0)

    # Location
    room_number = models.CharField(max_length=50, blank=True)
    venue_section = models.CharField(max_length=100, blank=True)
    is_virtual = models.BooleanField(default=False)
    virtual_meeting_link = models.URLField(max_length=500, blank=True)

    # Speakers/Presenters
    speakers = models.ManyToManyField(
        'AttendeeUser',
        related_name='speaking_sessions',
        blank=True
    )
    speaker_notes = models.TextField(blank=True)

    # Materials
    presentation_file = models.FileField(
        upload_to='session_materials/',
        null=True,
        blank=True
    )
    handouts = models.FileField(
        upload_to='session_handouts/',
        null=True,
        blank=True
    )

    # Additional Features
    is_featured = models.BooleanField(default=False)
    requires_additional_fee = models.BooleanField(default=False)
    additional_fee_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )

    # Categories and Tags
    categories = models.CharField(max_length=200, blank=True)
    tags = models.CharField(max_length=200, blank=True)

    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date_event']
        indexes = [
            models.Index(fields=['session_type']),
            models.Index(fields=['start_date_event']),
        ]

    def get_current_attendee_count(self):
        """Get the current number of registered attendees."""
        return self.registered_attendees.count()

    def is_full(self):
        """Check if the session is at capacity."""
        return self.get_current_attendee_count() >= self.max_attendee

    def get_available_spots(self):
        """Get the number of available spots."""
        return self.max_attendee - self.get_current_attendee_count()

    def is_registration_open(self):
        """Check if registration is currently open."""
        now = timezone.now()
        return self.start_date_register <= now <= self.end_date_register

    def add_speaker(self, user):
        """Add a speaker to the session."""
        self.speakers.add(user)

    def remove_speaker(self, user):
        """Remove a speaker from the session."""
        self.speakers.remove(user)

    def get_session_details(self):
        """Get comprehensive session details."""
        return {
            'name': self.session_name,
            'type': self.session_type,
            'timing': {
                'start': self.start_date_event,
                'end': self.end_date_event,
            },
            'capacity': {
                'max': self.max_attendee,
                'current': self.get_current_attendee_count(),
                'available': self.get_available_spots(),
            },
            'speakers': list(self.speakers.all()),
            'location': self.room_number or 'Virtual' if self.is_virtual else None,
        }

    def __str__(self):
        return f"{self.session_name} - {self.event.event_name}"

