from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator, URLValidator, EmailValidator
from django.utils import timezone
from decimal import Decimal

class Organizer(models.Model):
    """
    Enhanced Organizer model for managing event organizers with additional
    professional details, verification, and analytics capabilities.
    """

    ORGANIZER_TYPE_CHOICES = [
        ('INDIVIDUAL', 'Individual'),
        ('COMPANY', 'Company'),
        ('NONPROFIT', 'Non-Profit Organization'),
        ('EDUCATIONAL', 'Educational Institution'),
        ('GOVERNMENT', 'Government Organization'),
    ]

    VERIFICATION_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    ]

    # Basic Information
    user = models.ForeignKey('AttendeeUser', on_delete=models.CASCADE)
    organizer_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(validators=[EmailValidator()])

    # Organization Details
    organization_type = models.CharField(
        max_length=20,
        choices=ORGANIZER_TYPE_CHOICES,
        default='INDIVIDUAL'
    )

    # Branding
    logo = models.ImageField(
        upload_to='organizer_logos/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    banner_image = models.ImageField(
        upload_to='organizer_banners/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    brand_color = models.CharField(max_length=7, default='#000000', help_text="Hex color code")

    # Detailed Information
    description = models.TextField(blank=True)
    mission_statement = models.TextField(blank=True)
    year_established = models.PositiveIntegerField(null=True, blank=True)

    # Contact Information
    contact_phone = models.CharField(max_length=50, blank=True)
    contact_email = models.EmailField(blank=True)
    support_email = models.EmailField(blank=True)

    # Address
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    # Social Media and Web Presence
    website = models.URLField(max_length=200, blank=True, validators=[URLValidator()])
    facebook_url = models.URLField(max_length=200, blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    instagram_handle = models.CharField(max_length=50, blank=True)
    linkedin_url = models.URLField(max_length=200, blank=True)
    youtube_channel = models.URLField(max_length=200, blank=True)

    # Legal Information
    tax_id = models.CharField(max_length=50, blank=True)
    business_registration_number = models.CharField(max_length=50, blank=True)
    legal_entity_name = models.CharField(max_length=200, blank=True)

    # Verification and Status
    is_verified = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='PENDING'
    )
    verification_date = models.DateTimeField(null=True, blank=True)
    verification_documents = models.FileField(
        upload_to='verification_documents/',
        null=True,
        blank=True
    )

    # Categories and Specializations
    event_categories = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated list of event categories"
    )
    specializations = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated list of specializations"
    )

    # Financial Information
    bank_account_name = models.CharField(max_length=200, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_swift_code = models.CharField(max_length=20, blank=True)

    # Analytics and Metrics
    total_events_organized = models.PositiveIntegerField(default=0)
    total_attendees = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    # Settings and Preferences
    default_event_settings = models.JSONField(
        default=dict,
        help_text="Default settings for new events"
    )
    notification_preferences = models.JSONField(
        default=dict,
        help_text="Notification preferences"
    )

    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organizer_name']),
            models.Index(fields=['verification_status']),
            models.Index(fields=['created_at']),
        ]

    def show_events(self, status=None):
        """
        Returns events organized by this organizer, optionally filtered by status.

        Args:
            status (str, optional): Filter events by status (upcoming, ongoing, finished)

        Returns:
            QuerySet: Filtered events
        """
        events = self.events.all()

        if status:
            now = timezone.now()
            if status.lower() == 'upcoming':
                return events.filter(start_date_event__gt=now)
            elif status.lower() == 'ongoing':
                return events.filter(start_date_event__lte=now, end_date_event__gte=now)
            elif status.lower() == 'finished':
                return events.filter(end_date_event__lt=now)

        return events

    def get_analytics(self, time_period=None):
        """
        Returns analytics for the organizer's events.

        Args:
            time_period (str, optional): Time period for analytics (week, month, year)

        Returns:
            dict: Analytics data
        """
        events = self.events.all()
        if time_period:
            start_date = timezone.now()
            if time_period == 'week':
                start_date -= timezone.timedelta(days=7)
            elif time_period == 'month':
                start_date -= timezone.timedelta(days=30)
            elif time_period == 'year':
                start_date -= timezone.timedelta(days=365)
            events = events.filter(created_at__gte=start_date)

        total_revenue = sum(event.ticket_price * event.current_number_attendee for event in events)

        return {
            'total_events': events.count(),
            'total_attendees': sum(event.current_number_attendee for event in events),
            'total_revenue': total_revenue,
            'average_attendees': events.count() and sum(event.current_number_attendee for event in events) / events.count() or 0,
        }

    def update_verification_status(self, status, verified_by=None):
        """Updates the verification status of the organizer."""
        self.verification_status = status
        if status == 'VERIFIED':
            self.is_verified = True
            self.verification_date = timezone.now()
        self.save()

    def get_upcoming_events_count(self):
        """Returns the count of upcoming events."""
        return self.events.filter(start_date_event__gt=timezone.now()).count()

    def get_total_revenue(self):
        """Calculates total revenue from all events."""
        return sum(
            event.ticket_price * event.current_number_attendee
            for event in self.events.all()
        )

    def update_analytics(self):
        """Updates analytics fields based on current data."""
        self.total_events_organized = self.events.count()
        self.total_attendees = sum(
            event.current_number_attendee for event in self.events.all()
        )
        self.save()

    def get_full_address(self):
        """Returns the complete address string."""
        address_parts = filter(None, [
            self.street_address,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ])
        return ", ".join(address_parts)

    def __str__(self) -> str:
        return f"Organizer: {self.organizer_name}"

