from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


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
        
        subject = 'EventEase Verify your email address'
        
        # Create a plain text message
        plain_message = f"Hi,\n\nPlease verify your email by visiting this link: {verification_url}\n\nIf you didn’t sign up, please ignore this email."
        
        # Create an HTML message
        html_message = f"""
        <html>
            <body>
                <p>Hi,</p>
                <p>Thank you for registering! Please click the link below to verify your email address:</p>
                <a href="{verification_url}">Verify Email</a>
                <p>If you didn’t sign up, please ignore this email.</p>
            </body>
        </html>
        """
        
        # Create a multipart message
        msg = MIMEMultipart('alternative')
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = user.email
        msg['Subject'] = subject
        
        # Attach both plain text and HTML versions of the message
        msg.attach(MIMEText(plain_message, 'plain'))
        msg.attach(MIMEText(html_message, 'html'))

        try:
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()  # Upgrade to secure connection
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.sendmail(msg['From'], [msg['To']], msg.as_string())
            print("Email sent successfully.")
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {e}")
        except Exception as e:
            print(f"Failed to send email: {e}")
