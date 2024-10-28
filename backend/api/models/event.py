from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator

class Event(models.Model):
    """
    Represents an event with enhanced fields for better event management.

    Additional fields include:
    - Event image and banner
    - Location details
    - Category and tags
    - Pricing information
    - Social media links
    - Event status and visibility
    """
    EVENT_CATEGORIES = [
        ('CONFERENCE', 'Conference'),
        ('WORKSHOP', 'Workshop'),
        ('SEMINAR', 'Seminar'),
        ('NETWORKING', 'Networking'),
        ('CONCERT', 'Concert'),
        ('SPORTS', 'Sports'),
        ('OTHER', 'Other'),
    ]
    # Existing fields
    event_name = models.CharField(max_length=100)
    organizer = models.ForeignKey('Organizer', on_delete=models.CASCADE, related_name='events')
    event_create_date = models.DateTimeField('Event Created At', default=timezone.now)
    start_date_event = models.DateTimeField('Event Start Date', null=False, blank=False)
    end_date_event = models.DateTimeField('Event End Date', null=False, blank=True)
    start_date_register = models.DateTimeField('Registration Start Date', default=timezone.now)
    end_date_register = models.DateTimeField('Registration End Date', null=False, blank=False)
    description = models.TextField(max_length=400) 
    max_attendee = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    # Image fields
    event_image = models.ImageField(
        upload_to='event_images/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )

    # Location fields
    venue_name = models.CharField(max_length=200, null=True, blank=True)
    street_address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    
    # Pricing
    is_free = models.BooleanField(default=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    expected_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Online events
    is_online = models.BooleanField(default=False)

    # Categorization
    category = models.CharField(max_length=50, choices=EVENT_CATEGORIES, default='OTHER')
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")

    # Additional details
    detailed_description = models.TextField(blank=True, help_text="Full event details including schedule")
    status = models.CharField(max_length=20, default='')

    # Contact information
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    # Social media
    website_url = models.URLField(max_length=200, blank=True)
    facebook_url = models.URLField(max_length=200, blank=True)
    twitter_url = models.URLField(max_length=200, blank=True)
    instagram_url = models.URLField(max_length=200, blank=True)

    min_age_requirement = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)],
        help_text="Minimum age required to attend the event"
    )
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    terms_and_conditions = models.TextField(blank=True)

    # Existing methods remain the same
    @property
    def current_number_attendee(self):
        return self.ticket_set.count()
    
    def get_event_status(self) -> str:
        """
        Get current event Status

        Returns:
            str: String of the current status of the event
        """
        now = timezone.now()
        if now < self.start_date_event:
            return "Upcoming"
        elif self.start_date_event <= now <= self.end_date_event:
            return "Ongoing"
        else:
            return "Finished"

    def available_spot(self) -> int:
        """
        Get availble spots left in an event

        Return:
            int: Number of slots available for the event
        """
        return self.max_attendee - self.current_number_attendee
    
    
    def is_max_attendee(self) -> bool:
        """
        Check if event is slots are full

        Return:
            bool: True if event is full on slots, False if event is not full
        """
        if self.current_number_attendee == self.max_attendee:
            return True
        return False
    
    def is_event_published(self) -> bool:
        """
        Check if event is published

        Return:
            bool: True if event is published  if not return False
        """
        now = timezone.now()
        return self.event_create_date <= now
    
    def is_valid_date(self) -> bool:
        return self.start_date_register <= self.end_date_register <= self.start_date_event <= self.end_date_event
        
    def can_register(self) -> bool:
        """
        Check if registered within register period.

        Return:
            bool: True if can register, False if cannot register
        """
        now = timezone.now()
        return self.start_date_register <= now < self.end_date_register

    def get_event_status(self) -> str:
        now = timezone.now()
        if now < self.start_date_event:
            return "Upcoming"
        elif self.start_date_event <= now <= self.end_date_event:
            return "Ongoing"
        else:
            return "Finished"

    # New methods
    def get_full_address(self):
        """Returns the complete address of the venue"""
        if self.is_online:
            return "Online Event"

        address_parts = filter(None, [
            self.venue_name,
            self.street_address,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ])
        return ", ".join(address_parts)

    def __str__(self) -> str:
        return f"Event: {self.event_name}"

