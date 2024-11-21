from abc import ABC, abstractmethod
from api.views.modules import *
from api.views.schemas.ticket_schema import *

class TicketStrategy(ABC):
    """
    Abstract class for ticket strategies.
    """
    @staticmethod
    def get_strategy(strategy_name):
        """Get the ticket strategy instance based on the provided strategy name.

        Args:
            strategy_name (str): The name of the strategy to retrieve.

        Returns:
            TicketStrategy: An instance of the corresponding ticket strategy class,
            or None if the strategy name is not found.
        """
        strategies = {
            'get_user_ticket': TicketGetUserTicket(),
            'get_ticket_detail': TicketGetTicketDetail(),
            'register_ticket': TicketRegisterStrategy(),
            'cancel_ticket': TicketDeleteStrategy(),
            'sent_reminder': TicketSendReminderStrategy(),
        }
        return strategies.get(strategy_name)
    
    @abstractmethod
    def execute(self, *arg, **kwargs):
        """Execute the ticket strategy with the given arguments.

        Args:
            *arg: Variable length argument list. The arguments passed to this method
                depend on the specific strategy being executed.
            **kwargs: Keyword argument dictionary. The keyword arguments passed to this
                method depend on the specific strategy being executed.

        Returns:
            The result of executing the strategy.
        """
        pass
    
class TicketGetUserTicket(TicketStrategy):
    """
    Get a list of tickets for a specific user.
    """
    
    def execute(self, user_id: int) -> Response:
        """
        Execute the get user ticket strategy with the given user ID.

        Args:
            user_id (int): The ID of the user for which to retrieve tickets.

        Returns:
            Response: A response containing a list of TicketResponseSchema objects,
            each containing detailed information about one of the user's tickets.

        Raises:
            404: If the user with the given ID does not exist.
        """
        try:
            user = AttendeeUser.objects.get(id=user_id)
            tickets = Ticket.objects.filter(
                attendee=user, register_date__lte=timezone.now()
            ).order_by("-register_date")
            response_data = [
                TicketResponseSchema(**ticket.get_ticket_details()) for ticket in tickets
            ]
            return Response(response_data, status=200)
        except AttendeeUser.DoesNotExist:
            logger.error(f"User with ID {user_id} does not exist.")
            return Response({'error': 'User not found'}, status=404)
        
        
class TicketGetTicketDetail(TicketStrategy):
    """
    Get detailed information about a specific ticket.
    """
    def execute(self, ticket_id: int) -> Response:
        """
        Execute the get ticket detail strategy with the given ticket ID.

        Args:
            ticket_id (int): The ID of the ticket for which to retrieve details.

        Returns:
            Response: A response containing the ticket details, or an error message if the
            ticket does not exist or if an error occurs during the retrieval process.

        Raises:
            404: If the ticket with the given ID does not exist.
            500: If an error occurs during the retrieval process.
        """
        try:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            return Response(TicketResponseSchema(
                **ticket.get_ticket_details()), status=200)
        except Http404:
            logger.error("Ticket with ID %d does not exist.", ticket_id)
            return Response({'error': 'Ticket not found'}, status=404)
        except Exception as error:
            logger.error("Error fetching ticket details: %s", str(error))
            return Response({'error': 'Internal server error'}, status=500)
        
        
class TicketRegisterStrategy(TicketStrategy):
    """
    Register for an event.
    """
    def validate_event_registration(self, event, user):
        """
        Validate that the given user can register for the given event.

        Raises a ValidationError if the event has reached maximum capacity, if the event is not open for registration, if the event is not currently open for registration, or if the user's email domain is not authorized to register for this event. Raises a PermissionDenied exception if the event is private and the user's email domain is not authorized to register for this event.

        Args:
            event (Event): The event for which to validate registration.
            user (User): The user attempting to register for the event.

        Raises:
            ValidationError: If registration is not allowed for any reason.
            PermissionDenied: If the event is private and the user's email domain is not authorized to register for this event.
        """
        if event.is_max_attendee():
            raise ValidationError("This event has reached the maximum number of attendees.")

        if not event.can_register():
            raise ValidationError("Registration for this event is not allowed.")

        if not event.is_registration_status_allowed():
            raise ValidationError(f"Registration for this event is {event.status_registeration.lower()} now.")

        if event.visibility == 'PRIVATE' and not event.is_email_allowed(user.email):
            raise PermissionDenied("Your email domain is not authorized to register for this event.")

        if user.age is None:
            raise ValidationError("Please set your birth date in account information.")
    
    def execute(self, request: HttpRequest, event_id: int) -> Response:
        """
        Execute the register for an event strategy with the given event ID.

        Args:
            request (HttpRequest): The request object containing the user making the request.
            event_id (int): The ID of the event for which to register.

        Returns:
            Response: A response containing the registration details, or an error message if the
            registration fails.

        Raises:
            400: If the registration fails due to invalid data.
            403: If the event is private and the user's email domain is not authorized to register for this event.
            500: If an error occurs during the registration process.
        """
        user = request.user
        event = get_object_or_404(Event, id=event_id)

        try:
            self.validate_event_registration(event, user)
        except ValidationError as validation_error:
            return Response({'error': validation_error.messages[0]}, status=400)
        except PermissionDenied as permission_error:
            return Response({'error': str(permission_error)}, status=403)

        ticket = Ticket(
            event=event,
            attendee=user,
            register_date=timezone.now(),
            status='ACTIVE',
            created_at=timezone.now(),
        )

        if not ticket.is_valid_min_age_requirement():
            return Response(
                {'error': f"You must be at least {event.min_age_requirement} years old to attend this event."},
                status=400
            )

        if ticket.is_organizer_join_own_event(user):
            return Response(
                {'error': "Organizer cannot register for their own event."},
                status=400
            )

        try:
            ticket.clean()
            ticket.save()

            notification_manager = TicketNotificationManager(ticket)
            notification_manager.send_registration_confirmation()
            return Response(TicketResponseSchema(
                **ticket.get_ticket_details()).dict(), status=201)

        except ValidationError as validation_error:
            return Response({'error': str(validation_error.messages[0])}, status=400)
        except Exception as error:
            logger.error("Error during ticket registration: %s", str(error))
            return Response({'error': 'Internal server error'}, status=500)


class TicketDeleteStrategy(TicketStrategy):
    """
    Delete a ticket.
    """
    def execute(self, request: HttpRequest, ticket_id: int) -> Response:
        """
        Cancel a ticket for the requesting user and send a cancellation notification email.

        Args:
            request (HttpRequest): The HTTP request object, containing user and request metadata.
            ticket_id (int): The ID of the ticket to be canceled.

        Returns:
            Response: A response indicating the success or failure of the ticket cancellation and email notification.

        Raises:
            404: If the ticket does not exist or belongs to a different user.
            500: If there is an error during the cancellation process or sending the email.
        """
        this_user = request.user
        try:
            ticket = Ticket.objects.get(id=ticket_id, attendee=this_user)
            # Send cancellation email before deleting the ticket
            try:
                notification_manager = TicketNotificationManager(ticket)
                notification_manager.send_cancellation_notification()
            except Exception as email_error:
                logger.error("Failed to send cancellation email: %s", email_error)
                return Response({'error': 'Failed to send cancellation email'}, status=500)

            ticket.delete()
            return Response({
                "success": f"Ticket with ID {ticket_id} has been canceled."
            }, status=200)

        except Ticket.DoesNotExist:
            logger.error("Ticket with ID %d does not exist or belongs to a different user.", ticket_id)
            return Response({
                "error": f"Ticket with ID {ticket_id} does not exist or you do not have permission to cancel it."
            }, status=404)
        except Exception as error:
            logger.error("Error during ticket cancellation: %s", error)
            return Response({'error': 'Internal server error'}, status=500)
        
        
class TicketSendReminderStrategy(TicketStrategy):
    """
    Send a reminder email to a specific ticket holder.
    """
    def execute(self, ticket_id):
        """
        Send a reminder email to the ticket holder with the given ticket ID.

        Args:
            ticket_id (int): The ID of the ticket for which the reminder email is requested.
        """
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.email_sent = True
        ticket.save()
        ticket.send_event_reminder()
        