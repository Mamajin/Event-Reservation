from django.conf import settings
from celery import shared_task
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging
import smtplib


logger = logging.getLogger(__name__)


class EmailVerification:
    @staticmethod
    def generate_verification_token(user):
        """
        Generates a verification token for the given user.

        The verification token is used in the verification email sent to the user.

        :param user: The user to generate the verification token for.
        :return: The verification token.
        """
        return default_token_generator.make_token(user)
    
    @staticmethod
    def send_verification_email(user, token):
        """
        Sends a verification email to the given user.

        The verification email contains a link with a verification token that the user
        can use to verify their email address.

        :param user: The user to send the verification email to.
        :param token: The verification token to include in the email.
        """
        user_id = urlsafe_base64_encode(force_bytes(user.id))
        verification_url = f"{settings.SITE_URL}api/users/verify-email/{user_id}/{token}"
        
        subject = 'EventEase Verify your email address'
        
        plain_message = f"Hi,\n\nPlease verify your email by visiting this link: {verification_url}\n\nIf you didn’t sign up, please ignore this email."
        
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
        
        msg = MIMEMultipart('alternative')
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = user.email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(plain_message, 'plain'))
        msg.attach(MIMEText(html_message, 'html'))

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
            logger.info("Email sent successfully to %s", user.email)
            

class TicketEmailService:
    """
    Handles email notifications for ticket-related actions
    """
        
    def send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send an email to a given recipient with the given subject and HTML content

        Args:
            to_email (str): The recipient's email address
            subject (str): The email subject
            html_content (str): The HTML content of the email

        Returns:
            bool: True if the email was sent successfully, False otherwise
        """

        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = settings.EMAIL_HOST_USER
            message['To'] = to_email
            
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.send_message(message)
            
            logger.info(f"Successfully sent email to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False


class TicketNotificationManager:
    """
    Manages ticket notifications for different events
    """
    def __init__(self, ticket):
        self.ticket = ticket
        self.event = ticket.event
        self.attendee = ticket.attendee
        self.email_service = TicketEmailService()

    def send_registration_confirmation(self) -> bool:
        """
        Sends a registration confirmation email to the attendee after a ticket has been registered.
        
        Returns:
            bool: True if the email was sent successfully, False otherwise
        """
        html_content = self._generate_registration_html()
        subject = f"Registration Confirmed - {self.event.event_name}"
        
        success = self.email_service.send_email(
            to_email=self.attendee.email,
            subject=subject,
            html_content=html_content
        )
        
        if success:
            self.ticket.email_sent = True
            self.ticket.save(update_fields=['email_sent'])
        
        return success

    def send_cancellation_notification(self) -> bool:
        """
        Sends a cancellation notification email to the attendee after a ticket has been cancelled.
        
        Returns:
            bool: True if the email was sent successfully, False otherwise
        """
        html_content = self._generate_cancellation_html()
        subject = f"Ticket Cancelled - {self.event.event_name}"
        
        return self.email_service.send_email(
            to_email=self.attendee.email,
            subject=subject,
            html_content=html_content
        )
    
    def send_reminder_notification(self) -> bool:
        """
        Sends a reminder notification email to the attendee a day before the event.
        
        Returns:
            bool: True if the email was sent successfully, False otherwise
        """        
        if not self.ticket.email_sent:
            return False  
        subject = f'Reminder: {self.ticket.event.event_name} is tomorrow!'
        message = self._generate_reminder_html()
        success = self.email_service.send_email(
            to_email=self.ticket.attendee.email,
            subject=subject,
            html_content=message
        )
        if success:
            self.ticket.email_sent = False
            self.ticket.save(update_fields=['email_sent'])
        return success

    def _generate_reminder_html(self) -> str:
        """
        Generate HTML content for the event reminder email.
        
        Returns:
            str: The rendered HTML content
        """
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #333;">Event Reminder</h2>
            <p>Dear {self.attendee.full_name},</p>
            <p>This is a reminder that <strong>{self.event.event_name}</strong> will take place tomorrow.</p>
            
            <div style="background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px;">
                <h3 style="margin-top: 0;">Event Details</h3>
                <p><strong>Event:</strong> {self.event.event_name}</p>
                <p><strong>Date:</strong> {self.event.start_date_event.strftime('%B %d, %Y %I:%M %p')}</p>
                <p><strong>Location:</strong> {self.event.address}</p>
            </div>
            
            <p>We look forward to seeing you there!</p>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                <small style="color: #666;">This is an automated message, please do not reply directly to this email.</small>
            </div>
        </div>
        """

    def _generate_registration_html(self) -> str:
        """
        Generate HTML content for the registration confirmation email.
        
        Returns:
            str: The rendered HTML content
        """
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #333;">Registration Confirmed</h2>
            <p>Dear {self.attendee.full_name},</p>
            <p>Your registration for <strong>{self.event.event_name}</strong> has been confirmed!</p>
            
            <div style="background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px;">
                <h3 style="margin-top: 0;">Event Details</h3>
                <p><strong>Event:</strong> {self.event.event_name}</p>
                <p><strong>Date:</strong> {self.event.start_date_event.strftime('%B %d, %Y %I:%M %p')}</p>
                <p><strong>Location:</strong> {self.event.address}</p>
                <p><strong>Ticket Number:</strong> {self.ticket.ticket_number}</p>
            </div>
            
            <div style="background-color: #e9ecef; padding: 20px; margin: 20px 0; border-radius: 5px;">
                <h3 style="margin-top: 0;">Important Information</h3>
                <p>{self.event.description}</p>
            </div>
            
            <p>Please keep your ticket number for reference: <strong>{self.ticket.ticket_number}</strong></p>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                <small style="color: #666;">This is an automated message, please do not reply directly to this email.</small>
            </div>
        </div>
        """

    def _generate_cancellation_html(self) -> str:
        """
        Generate HTML content for the cancellation confirmation email.
        
        Returns:
            str: The rendered HTML content
        """
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #333;">Ticket Cancellation Confirmation</h2>
            <p>Dear {self.attendee.full_name},</p>
            <p>Your ticket for <strong>{self.event.event_name}</strong> has been cancelled.</p>
            
            <div style="background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px;">
                <h3 style="margin-top: 0;">Cancellation Details</h3>
                <p><strong>Event:</strong> {self.event.event_name}</p>
                <p><strong>Ticket Number:</strong> {self.ticket.ticket_number}</p>
                <p><strong>Cancellation Date:</strong> {timezone.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <p>If you have any questions about this cancellation, please contact our support team.</p>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                <small style="color: #666;">This is an automated message, please do not reply directly to this email.</small>
            </div>
        </div>
        """

@shared_task
def send_reminder_emails():
    """
    Sends reminder emails to attendees with tickets for events occurring tomorrow.

    This task queries for tickets associated with events starting the next day
    and sends reminder emails to those attendees whose `email_sent` flag is set to True.

    The task iterates over each ticket meeting the criteria, creates a 
    TicketNotificationManager instance, and invokes the send_reminder_notification 
    method to dispatch the reminder email.
    """
    from api.models.ticket import Ticket
    tomorrow = timezone.now() + timedelta(days=1)
    tickets = Ticket.objects.filter(
        event__start_date_event__date=tomorrow.date(),
        email_sent=True
    )

    for ticket in tickets:
        notification_manager = TicketNotificationManager(ticket)
        notification_manager.send_reminder_notification()
        