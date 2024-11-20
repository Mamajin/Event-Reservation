from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from api.utils import EmailVerification


class AttendeeUser(AbstractUser):
    """
    Enhanced user model for event attendees with additional profile information,
    preferences, and social features.
    """
    
    # Personal Information
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)  # Optional field
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    birth_date = models.DateField('Birth Date', null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=False, ) # Max number
    status = models.CharField(max_length=50, null=True, blank=True, default='Attendee')
    email = models.EmailField(unique=True, null=False, blank=False) 
    address = models.CharField(max_length=500, null = True, blank = True, default= " ")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null = True, blank= True, default= 0.00)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null = True, blank= True, default= 0.00)

    # Profile Picture
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        storage=default_storage,
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
    
    is_email_verified = models.BooleanField(default=False)
    email_verification_token_sent_at = models.DateTimeField(null=True, blank=True)
    
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
        if self.birth_date:
            today = timezone.now().date()
            age = today.year - self.birth_date.year
            if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
                age -= 1
            return age
        return None

    @property
    def full_name(self):
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def profile_picture_url(self):
        """Return the user profile picture if has."""
        if self.profile_picture:
            return self.profile_picture.url
        return None
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email  # Set username to email if not provided
        super().save(*args, **kwargs)
                
    def send_verification_email(self):
        """Generate and send verification email with a secure token."""
        token = EmailVerification.generate_verification_token(self)

        self.email_verification_token_sent_at = timezone.now()
        self.save()
        
        EmailVerification.send_verification_email(self, token)

    def __str__(self):
        return f"{self.full_name} ({self.email})"

