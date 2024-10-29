from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import FileExtensionValidator, EmailValidator
from django.utils.translation import gettext_lazy as _


class AttendeeUser(AbstractUser):
    """
    Enhanced user model for event attendees with additional profile information,
    preferences, and social features.
    """
    
    # Personal Information
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    birth_date = models.DateField('Birth Date', null=False, blank=False)
    phone_number = models.CharField(max_length=50, null=False, blank=False, ) # Max number
    status = models.CharField(max_length=50, null=True, blank=True, default='Attendee')

    # Profile Picture
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )

    # Professional Information
    company = models.CharField(max_length=200, blank=True)

    # Social Media
    facebook_profile = models.URLField(max_length=200, blank=True)
    instagram_handle = models.CharField(max_length=50, blank=True)


    nationality = models.CharField(
        max_length=100,
        blank=False,
        default='',
    )
    
    attended_events_count = models.PositiveIntegerField(default=0)
    cancelled_events_count = models.PositiveIntegerField(default=0)

    # System Fields
    created_at = models.DateTimeField('Created At', default=timezone.now)
    updated_at = models.DateTimeField('Updated At', auto_now=True)

    # Required for Django's auth
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='attendeeuser_set',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='attendeeuser_set',
        blank=True,
    )


    @property
    def age(self):
        today = timezone.now().date()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    @property
    def full_name(self):
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}"

    def get_upcoming_events(self):
        """Returns all upcoming events the user is registered for."""
        return self.ticket_set.filter(
            event__start_date_event__gt=timezone.now()
        ).order_by('event__start_date_event')

    def get_past_events(self):
        """Returns all past events the user has attended."""
        return self.ticket_set.filter(
            event__end_date_event__lt=timezone.now()
        ).order_by('-event__end_date_event')

    def update_event_counts(self):
        """Updates the attended and cancelled event counts."""
        self.attended_events_count = self.ticket_set.filter(
            event__end_date_event__lt=timezone.now()
        ).count()
        self.save()

    def __str__(self):
        return f"{self.full_name} ({self.email})"

