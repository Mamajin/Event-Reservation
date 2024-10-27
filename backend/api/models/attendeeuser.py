from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, FileExtensionValidator, EmailValidator
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
    phone_number = models.CharField(max_length=50, null=False, blank=False)

    # Profile Picture
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )

    # Additional Contact Information
    secondary_email = models.EmailField(
        _('Secondary Email'),
        blank=True,
        validators=[EmailValidator()]
    )
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=50, blank=True)

    # Address Information
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    # Professional Information
    company = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=200, blank=True)
    industry = models.CharField(max_length=200, blank=True)
    professional_bio = models.TextField(blank=True)

    # Social Media
    linkedin_profile = models.URLField(max_length=200, blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    facebook_profile = models.URLField(max_length=200, blank=True)
    instagram_handle = models.CharField(max_length=50, blank=True)
    website = models.URLField(max_length=200, blank=True)

    # Preferences
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('zh', 'Chinese'),
        ('th', 'Thai')
    ]

    TIMEZONE_CHOICES = [
        ('UTC', 'UTC'),
        ('US/Pacific', 'US/Pacific'),
        ('US/Eastern', 'US/Eastern'),
        ('Europe/London', 'Europe/London'),
        ('Asia/Tokyo', 'Asia/Tokyo'),
    ]

    preferred_language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='en'
    )

    timezone = models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES,
        default='UTC'
    )

    # Communication Preferences
    receive_email_notifications = models.BooleanField(default=True)
    receive_sms_notifications = models.BooleanField(default=False)
    receive_marketing_emails = models.BooleanField(default=True)

    # Dietary Preferences
    DIETARY_CHOICES = [
        ('NONE', 'No Restrictions'),
        ('VEGETARIAN', 'Vegetarian'),
        ('VEGAN', 'Vegan'),
        ('HALAL', 'Halal'),
        ('KOSHER', 'Kosher'),
        ('GLUTEN_FREE', 'Gluten Free'),
        ('DAIRY_FREE', 'Dairy Free'),
    ]

    dietary_preferences = models.CharField(
        max_length=20,
        choices=DIETARY_CHOICES,
        default='NONE'
    )
    food_allergies = models.TextField(blank=True)

    # Accessibility Needs
    accessibility_requirements = models.TextField(
        blank=True,
        help_text="Please specify any accessibility requirements"
    )

    # Account Status and Verification
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    account_status = models.CharField(
        max_length=20,
        choices=[
            ('ACTIVE', 'Active'),
            ('SUSPENDED', 'Suspended'),
            ('INACTIVE', 'Inactive')
        ],
        default='ACTIVE'
    )

    # Event Related
    interests = models.TextField(
        blank=True,
        help_text="Comma-separated list of interests for event recommendations"
    )
    attended_events_count = models.PositiveIntegerField(default=0)
    cancelled_events_count = models.PositiveIntegerField(default=0)

    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    class Meta:
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
        ]

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

    def get_full_address(self):
        """Returns the user's full address."""
        address_parts = filter(None, [
            self.street_address,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ])
        return ", ".join(address_parts)

    def update_event_counts(self):
        """Updates the attended and cancelled event counts."""
        self.attended_events_count = self.ticket_set.filter(
            event__end_date_event__lt=timezone.now()
        ).count()
        self.save()

    def verify_account(self):
        """Marks the account as verified."""
        self.is_verified = True
        self.verification_date = timezone.now()
        self.save()

    def get_event_recommendations(self):
        """Returns recommended events based on user interests and history."""
        from api.models.event import Event  # Import here to avoid circular import
        interests_list = [i.strip() for i in self.interests.split(',') if i.strip()]

        return Event.objects.filter(
            start_date_event__gt=timezone.now(),
            tags__in=interests_list
        ).distinct()

    def __str__(self):
        return f"{self.full_name} ({self.email})"

