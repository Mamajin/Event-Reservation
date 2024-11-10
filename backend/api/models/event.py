from django.db import models
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from api.models.organizer import Organizer
import re


# class EventManager(models.Manager):
#     def public(self):
#         return self.filter(visibility='PUBLIC')

#     def private(self):
#         return self.filter(visibility='PRIVATE')
    
#     def filter_by_category(self, category):
#         return self.filter(category=category)
    
#     def within_date_range(self, start_date, end_date):
#         return self.filter(start_date_event__gte=start_date, end_date_event__lte=end_date)


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
    DRESS_CODES = [
        ('CASUAL', 'Casual'),
        ('SMART_CASUAL', 'Smart Casual'),
        ('BUSINESS_CASUAL', 'Business Casual'),
        ('SEMI_FORMAL', 'Semi-Formal'),
        ('FORMAL', 'Formal'),
        ('BLACK_TIE', 'Black Tie'),
        ('WHITE_TIE', 'White Tie'),
        ('THEMED', 'Themed Dress Code'),
        ('OUTDOOR_BEACH_CASUAL', 'Outdoor/Beach Casual'),
    ]
    STATUS_OF_REGISTRATION = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('FULL', 'Full'),
        ('PENDING', 'Pending'),
        ('CANCELLED', 'Cancelled'),
        ('WAITLIST', 'Waitlist'),
    ]
    EVENT_VISIBILITY = [
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private')
    ]
    # Existing fields
    event_name = models.CharField(max_length=100)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='events')
    event_create_date = models.DateTimeField('Event Created At', default=timezone.now)
    start_date_event = models.DateTimeField('Event Start Date', null=False, blank=False)
    end_date_event = models.DateTimeField('Event End Date', null=False, blank=True)
    start_date_register = models.DateTimeField('Registration Start Date', default=timezone.now)
    end_date_register = models.DateTimeField('Registration End Date', null=False, blank=False)
    description = models.TextField(max_length=400) 
    max_attendee = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    address = models.CharField(max_length=500, null = True, blank = True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null = True, blank= True, default= 0.00)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null = True, blank= True, default= 0.00)

    # Image fields
    event_image = models.ImageField(
        upload_to='event_images/',
        storage=default_storage,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )
    
    # Pricing
    is_free = models.BooleanField(default=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    expected_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Online events
    is_online = models.BooleanField(default=False)
    meeting_link = models.TextField(max_length=500, null=True, blank=True)

    # Categorization
    category = models.CharField(max_length=50, choices=EVENT_CATEGORIES, default='OTHER')
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    
    # Privacy settings
    visibility = models.CharField(
        max_length=20,
        choices=EVENT_VISIBILITY,
        default='PUBLIC',
        help_text='Choose whether the event is public or private'
    )
    allowed_email_domains = models.TextField(
        null=True,
        blank=True,
        help_text="Comma-separated list of allowed email domains (e.g., 'ku.th, example.com')"
    )

    # Additional details
    detailed_description = models.TextField(blank=True, help_text="Full event details including schedule")
    status = models.CharField(max_length=20, default='')
    dress_code = models.CharField(max_length=20, choices = DRESS_CODES, null = False, blank = False, default= "CASUAL")
    status_registeration = models.CharField(max_length=20, choices= STATUS_OF_REGISTRATION, null = False, blank= False)

    # Contact information
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    # Social media
    website_url = models.URLField(max_length=200, null=True, blank=True)
    facebook_url = models.URLField(max_length=200, null=True, blank=True)
    twitter_url = models.URLField(max_length=200, null=True, blank=True)
    instagram_url = models.URLField(max_length=200, null=True, blank=True)

    min_age_requirement = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)],
        help_text="Minimum age required to attend the event"
    )
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    terms_and_conditions = models.TextField(null=True, blank=True)
    
    # objects = EventManager()

    # Existing methods remain the same
    @property
    def current_number_attendee(self):
        """
        Get the total Event's ticket number.
        """
        return self.ticket_set.count()
    
    @property
    def like_count(self):
        """
        Get the total Event's likes.
        """
        return self.likes.count()
    
    @property
    def bookmark_count(self):
        """
        Get the total Event's bookmarks.
        """
        return self.bookmarks_set.count() 
    

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
    
    def is_email_allowed(self, email: str) -> bool:
        """
        Check if an email address is allowed to register for this event
        based on the domain restrictions.

        Args:
            email (str): Email address to check

        Returns:
            bool: True if email is allowed, False otherwise
        """
        if self.visibility == 'PUBLIC' or not self.allowed_email_domains:
            return True
        try:
            domain = email.split('@')[1].lower()
        except IndexError:
            return False
        allowed_domains = [
            d.strip().lower()
            for d in self.allowed_email_domains.split(',')
            if d.strip()
        ]

        return domain in allowed_domains

    def clean(self):
        super().clean()
        if self.visibility == 'PRIVATE' and self.allowed_email_domains:
            domains = [d.strip() for d in self.allowed_email_domains.split(',')]
            invalid_domains = [d for d in domains if not re.match(r'^[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*$', d)]
            if invalid_domains:
                raise ValidationError({
                    'allowed_email_domains': f"Invalid domain(s): {', '.join(invalid_domains)}"
                })
        if self.start_date_event >= self.end_date_event:
            raise ValidationError("End date must be after start date.")


    def __str__(self) -> str:
        return f"Event: {self.event_name}"
