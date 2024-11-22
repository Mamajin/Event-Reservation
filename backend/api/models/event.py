import re
from django.db import models
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from api.models.organizer import Organizer


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
    ]
    EVENT_VISIBILITY = [
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private')
    ]
    VERIFICATION_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
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
    max_attendee = models.PositiveIntegerField(default = None, null = True, blank= True)
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
    status_registeration = models.CharField(max_length=20, choices= STATUS_OF_REGISTRATION, null = False, blank= False, default= "OPEN")
    # Contact information
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    # Social media
    website_url = models.URLField(max_length=200, null=True, blank=True)
    facebook_url = models.URLField(max_length=200, null=True, blank=True)
    twitter_url = models.URLField(max_length=200, null=True, blank=True)
    instagram_url = models.URLField(max_length=200, null=True, blank=True)
    other_url = models.URLField(max_length=1000, null=True, blank=True, help_text='Other social media URL. Separated by comma eg. https://www.example.com, https://www.example2.com')

    min_age_requirement = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)],
        help_text="Minimum age required to attend the event"
    )
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    is_verified = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='PENDING'
    )
    
    terms_and_conditions = models.TextField(null=True, blank=True)

        
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
        return self.likes.filter(status='like').count()
    
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
        if self.max_attendee == 0:
            return self.current_number_attendee
        return self.max_attendee - self.current_number_attendee  
    
    def is_max_attendee(self) -> bool:
        """
        Check if event is slots are full

        Return:
            bool: True if event is full on slots, False if event is not full
        """
        if self.max_attendee == 0:
            return False
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
    
    def is_registration_status_allowed(self) -> bool:
        """Check if the registration status is allowed to register."""
        return self.status_registeration not in ('CLOSED', 'FULL')
    
    def set_status_event(self):
        """
        Set the status of the event based on the current date and time.

        The status can be 'UPCOMING', 'ONGOING', or 'COMPLETED' depending on
        whether the current time is before the event start, during the event,
        or after the event has ended.
        """
        now = timezone.now()  
        
        if now < self.start_date_event:
            self.status = 'UPCOMING'  
        elif now < self.end_date_event:
            self.status = 'ONGOING'  
        else:
            self.status = 'COMPLETED'
            
    def set_registeration_status(self):
        """
        Set the status of the event registration based on the current date and time.

        The status can be 'CLOSED', 'FULL', or 'OPEN' depending on whether the current time is
        after the event registration end date, whether the maximum number of attendee has been
        reached, or neither of the above has occurred.

        The function will save the event object after setting the status.
        """
        if not self.end_date_register:
            raise ValueError("End date of registration cannot be null")
        now = timezone.now()
        if self.max_attendee:
            if self.current_number_attendee >= self.max_attendee:
                self.status_registeration = "FULL"
        elif now > self.end_date_register:
            self.status_registeration = "CLOSED"
        else:
            self.status_registeration = "OPEN"
        self.save()
 
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
        """
        Validate the event data.

        This method is called by the model's full_clean() method and is used to
        validate the data before saving it to the database.

        Raises:
            ValidationError: If the allowed email domains contain invalid domains.
            ValidationError: If the end date is not after the start date.
        """
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
        """
        Return a string representation of the event, displaying its name.
        """
        return f"Event: {self.event_name}"
