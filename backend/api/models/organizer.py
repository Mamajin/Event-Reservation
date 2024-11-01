from django.db import models
from django.core.validators import FileExtensionValidator, EmailValidator
from django.utils import timezone
from api.models.user import AttendeeUser
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
    user = models.ForeignKey(AttendeeUser, on_delete=models.CASCADE)
    organizer_name = models.CharField(max_length=100)
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
    
    
    def show_event(self):
        """
        Returns all events an Organizer has ever organized both active and closed
        events

        Returns:
            query_set: List of events an organizer have organized
        """
        return Organizer.events_set.all()
    
    def is_organizer(self, this_user):
        """
        Check if a given user is an organizer.

        Args:
            this_user (AttendeeUser): The user to check.

        Returns:
            bool: True if the user is an organizer, otherwise False.
        """
        return Organizer.objects.filter(user=this_user).exists()
    
    def organizer_name_is_taken(self, name):
        """
        Check if an organizer name is already taken.

        Args:
            name (str): The name to check.

        Returns:
            bool: True if the name is taken, otherwise False.
        """
        return Organizer.objects.filter(organizer_name=name).exists()

    def update_verification_status(self, status, verified_by=None):
        """Updates the verification status of the organizer."""
        self.verification_status = status
        if status == 'VERIFIED':
            self.is_verified = True
            self.verification_date = timezone.now()
        self.save()

    def __str__(self) -> str:
        return f"Organizer: {self.organizer_name}"

