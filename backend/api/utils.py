from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

class EmailVerification:
    @staticmethod
    def generate_verification_token(user):
        """Generate a secure verification token tied to the user instance."""
        return default_token_generator.make_token(user)
    
    @staticmethod
    def send_verification_email(user, token):
        """Send an HTML verification email to the user."""
        user_id = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = f"{settings.SITE_URL}/api/verify-email/{user_id}/{token}"
        
        subject = 'Verify your email address'
        html_content = render_to_string('email_verification.html', {'verification_url': verification_url, 'user': user})
        
        send_mail(
            subject,
            '',  # Empty plain text body
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_content,  # Use HTML content
            fail_silently=False,
        )
