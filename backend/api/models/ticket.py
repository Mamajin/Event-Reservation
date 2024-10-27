from django.db import models
from django.utils import timezone
from decimal import Decimal


class Ticket(models.Model):
    """
    Enhanced Ticket model for managing event attendance with additional features
    for ticket types, pricing, and status tracking.
    """

    TICKET_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CHECKED_IN', 'Checked In'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    ]

    TICKET_TYPE_CHOICES = [
        ('GENERAL', 'General Admission'),
        ('VIP', 'VIP'),
        ('EARLY_BIRD', 'Early Bird'),
        ('STUDENT', 'Student'),
        ('GROUP', 'Group'),
        ('VIRTUAL', 'Virtual Attendance'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    # Basic Information
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    attendee = models.ForeignKey('AttendeeUser', on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=50, unique=True)
    register_date = models.DateTimeField('Date registered', default=timezone.now)

    # Ticket Details
    ticket_type = models.CharField(
        max_length=20,
        choices=TICKET_TYPE_CHOICES,
        default='GENERAL'
    )
    status = models.CharField(
        max_length=20,
        choices=TICKET_STATUS_CHOICES,
        default='PENDING'
    )

    # Pricing Information
    price_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    discount_code = models.CharField(max_length=50, blank=True)
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )

    # Payment Information
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING'
    )
    payment_method = models.CharField(max_length=50, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)

    # Check-in Information
    is_checked_in = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)
    checked_in_by = models.ForeignKey(
        'AttendeeUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checked_in_tickets'
    )

    # Additional Information
    seat_number = models.CharField(max_length=50, blank=True)
    special_requirements = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    # Session Registration
    registered_sessions = models.ManyToManyField(
        'Session',
        blank=True,
        related_name='registered_attendees'
    )

    # Cancellation/Refund
    cancellation_date = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    refund_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    refund_date = models.DateTimeField(null=True, blank=True)

    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-register_date']
        indexes = [
            models.Index(fields=['ticket_number']),
            models.Index(fields=['status']),
            models.Index(fields=['register_date']),
        ]

    def check_in(self, checked_in_by=None):
        """Process check-in for the ticket."""
        if not self.is_checked_in:
            self.is_checked_in = True
            self.check_in_time = timezone.now()
            self.checked_in_by = checked_in_by
            self.status = 'CHECKED_IN'
            self.save()
            return True
        return False

    def cancel_ticket(self, reason=None):
        """Cancel the ticket and initiate refund process if applicable."""
        self.status = 'CANCELLED'
        self.cancellation_date = timezone.now()
        self.cancellation_reason = reason
        self.save()

        if self.payment_status == 'COMPLETED':
            self.initiate_refund()

    def initiate_refund(self):
        """Initiate refund process for the ticket."""
        self.payment_status = 'REFUNDED'
        self.refund_amount = self.price_paid
        self.refund_date = timezone.now()
        self.save()

    def register_for_session(self, session):
        """Register the ticket holder for a session."""
        if session.event == self.event and not session.is_full():
            self.registered_sessions.add(session)
            return True
        return False

    def get_ticket_details(self):
        """Get comprehensive ticket details."""
        return {
            'ticket_number': self.ticket_number,
            'event': self.event.event_name,
            'attendee': self.attendee.full_name,
            'ticket_type': self.ticket_type,
            'status': self.status,
            'price_paid': self.price_paid,
            'is_checked_in': self.is_checked_in,
            'registered_sessions': list(self.registered_sessions.all()),
        }

    def __str__(self) -> str:
        return f"Ticket: {self.ticket_number} - {self.event.event_name}"