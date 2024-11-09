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
        user_id = urlsafe_base64_encode(force_bytes(user.id))
        verification_url = f"{settings.SITE_URL}api/users/verify-email/{user_id}/{token}"
        
        subject = 'Verify your email address'
        plain_message = f"Hi, please verify your email by visiting this link: {verification_url}"
        message = f"""
        <html>
            <body>
                <p>Hi,</p>
                <p>Thank you for registering! Please click the link below to verify your email address:</p>
                <a href="{verification_url}">Verify Email</a>
                <p>If you didn’t sign up, please ignore this email.</p>
            </body>
        </html>
        """
        
        send_mail(
            subject,
            plain_message,  # Empty plain text body
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=message,
            fail_silently=False,  # Use HTML content
        )
