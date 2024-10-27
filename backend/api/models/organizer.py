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

    # Detailed Information
    description = models.TextField(blank=True)

    # Contact Information
    # contact_phone = models.CharField(max_length=50, blank=True)
    # contact_email = models.EmailField(blank=True)
    # support_email = models.EmailField(blank=True)

    # Address
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    # Social Media and Web Presence
    facebook_url = models.URLField(max_length=200, blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    instagram_handle = models.CharField(max_length=50, blank=True)
    youtube_channel = models.URLField(max_length=200, blank=True)

    # Verification and Status
    is_verified = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='PENDING'
    )

    # System Fields
    created_at = models.DateTimeField('Created At', default=timezone.now)
    updated_at = models.DateTimeField('Updated At', auto_now=True)

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

    def update_verification_status(self, status, verified_by=None):
        """Updates the verification status of the organizer."""
        self.verification_status = status
        if status == 'VERIFIED':
            self.is_verified = True
            self.verification_date = timezone.now()
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

