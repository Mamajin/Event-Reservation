from django.db import models
from django.utils import timezone
from decimal import Decimal


class Ticket(models.Model):
    """
    Enhanced Ticket model for managing event attendance with additional features
    for ticket types, pricing, and status tracking.
    """

    # Basic Information
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    attendee = models.ForeignKey('AttendeeUser', on_delete=models.CASCADE)
    register_date = models.DateTimeField('Date registered', default=timezone.now)

    status = models.CharField(
        max_length=20,
        default=''
    )

    # Cancellation/Refund
    cancellation_date = models.DateTimeField(null=True, blank=True)

    # System Fields
    created_at = models.DateTimeField('Created At', default=timezone.now)
    updated_at = models.DateTimeField('Updated At', auto_now=True)


    def cancel_ticket(self, reason=None):
        """Cancel the ticket and initiate refund process if applicable."""
        self.status = 'CANCELLED'
        self.cancellation_date = timezone.now()
        self.cancellation_reason = reason
        self.save()

    def get_ticket_details(self):
        """Get comprehensive ticket details."""
        return {
            'ticket_number': self.ticket_number,
            'event': self.event.event_name,
            'attendee': self.attendee.full_name,
            'ticket_type': self.ticket_type,
            'status': self.status,
        }

    def __str__(self) -> str:
        return f"Ticket: {self.ticket_number} - {self.event.event_name}"