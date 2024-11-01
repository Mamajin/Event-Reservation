from typing import Optional, Dict
from django.db import models
from django.utils import timezone
import random
import string
from pydantic import ValidationError
from api.models.organizer import Organizer


class Ticket(models.Model):
    """
    Enhanced Ticket model for managing event attendance with additional features
    for ticket types, pricing, and status tracking.
    """

    # Basic Information
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    attendee = models.ForeignKey('AttendeeUser', on_delete=models.CASCADE)
    register_date = models.DateTimeField('Date registered', default=timezone.now)

    TICKET_STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('CANCELLED', 'Cancelled'),
        ('EXPIRED', 'Expired'),
    ] 
    status = models.CharField(
        max_length=20,
        choices=TICKET_STATUS_CHOICES,
        default='ACTIVE'
    )

    ticket_number = models.CharField(max_length=100, unique=True, default='', editable=False)
    
    # Cancellation/Refund
    cancellation_date = models.DateTimeField(null=True, blank=True)

    # System Fields
    created_at = models.DateTimeField('Created At', default=timezone.now)
    updated_at = models.DateTimeField('Updated At', auto_now=True)


    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ticket_number']),
            models.Index(fields=['status']),
            models.Index(fields=['register_date']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'attendee'],
                name='unique_event_attendee'
            )
        ]

    def save(self, *args, **kwargs):
        """Override save method to handle ticket number generation and validation."""
        if not self.ticket_number:
            self.ticket_number = self.generate_ticket_number()
        
        if self.status == 'CANCELLED' and not self.cancellation_date:
            self.cancellation_date = timezone.now()
            
        super().save(*args, **kwargs)

    def clean(self):
        """Validate the ticket before saving."""
        if self.is_user_register_the_same_event():
            raise ValidationError("User has already registered for this event.")
            
        if self.is_organizer_join_own_event(self.attendee):
            raise ValidationError("Organizer cannot register for their own event.")

    def cancel_ticket(self, reason: Optional[str] = None) -> None:
        """
        Cancel the ticket and record cancellation details.

        Args:
            reason (str, optional): Reason for cancellation
        """
        if self.status == 'CANCELLED':
            raise ValidationError("Ticket is already cancelled.")
            
        self.status = 'CANCELLED'
        self.cancellation_date = timezone.now()
        self.save()

    def get_ticket_details(self) -> Dict:
        """
        Get comprehensive ticket details.

        Returns:
            Dict: Dictionary containing ticket details
        """
        return {
            "id": self.id,
            "ticket_number": self.ticket_number,
            "event_id": self.event.id,
            "fullname": self.attendee.full_name,
            "register_date": self.register_date,
            "status": self.status,
            'cancellation_date': self.cancellation_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
    def generate_ticket_number(self) -> str:
        """
        Generate a random, unique ticket number.

        Returns:
            str: Generated ticket number
        """
        while True:
            prefix = "TICKET"
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            ticket_number = f"{prefix}-{random_string}"
            
            # Check if ticket number already exists
            if not Ticket.objects.filter(ticket_number=ticket_number).exists():
                return ticket_number
        
    def is_user_registered(self, user) -> bool:
        """
        Check if a user is registered for any event.

        Args:
            user (AttendeeUser): User to check

        Returns:
            bool: True if user is registered, False otherwise
        """
        return Ticket.objects.filter(attendee=user).exists()
        
    def is_organizer_join_own_event(self, user) -> bool:
        """
        Check if an organizer is trying to join their own event.

        Args:
            user (User): User to check

        Returns:
            bool: True if user is the organizer of the event, False otherwise
        """
        try:
            organizer = Organizer.objects.get(user=user)
            return self.event.organizer == organizer
        except Organizer.DoesNotExist:
            return False
    
    def is_user_register_the_same_event(self) -> bool:
        """
        Check if user is already registered for this event.

        Returns:
            bool: True if user is already registered, False otherwise
        """
        return Ticket.objects.filter(
            attendee=self.attendee,
            event=self.event,
            status='ACTIVE'
        ).exists()
    
    def get_ticket_status(self) -> str:
        """
        Get the current status of the ticket.

        Returns:
            str: Current ticket status
        """
        if self.status == 'ACTIVE':
            # Check if event has passed
            if self.event.event_date < timezone.now():
                self.status = 'EXPIRED'
                self.save()
        return self.status

    def __str__(self) -> str:
        """String representation of the ticket."""
        return f"Ticket: {self.ticket_number} - {self.event.event_name}"