from abc import ABC, abstractmethod
from api.views.modules import *
from api.views.schemas import *

class TicketStrategy(ABC):
    
    @staticmethod
    def get_strategy(strategy_name):
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
        pass
    
class TicketGetUserTicket(TicketStrategy):

    
    def execute(self,id):
        try:
            user = AttendeeUser.objects.get(id= id)
            tickets = Ticket.objects.filter(attendee=user, register_date__lte=timezone.now()).order_by("-register_date")
            return [
                TicketResponseSchema(
                    **ticket.get_ticket_details()
                ) for ticket in tickets
            ]
        except AttendeeUser.DoesNotExist:
            logger.error(f"User with ID {id} does not exist.")
            return Response({'error': 'User not found'}, status=404)
        
        
class TicketGetTicketDetail(TicketStrategy):
    
    def execute(self,id):
        """
        Get detailed information about a specific ticket.
        """
        try:
            ticket = get_object_or_404(Ticket, id=id)
            return Response(TicketResponseSchema(
                **ticket.get_ticket_details()), status=200)
            
        except Http404:
            logger.error(f"Ticket with ID {id} does not exist.")
            return Response({'error': 'Ticket not found'}, status=404)
        except Exception as e:
            logger.error(f"Error fetching ticket details: {str(e)}")
            return Response({'error': 'Internal server error'}, status=500)
        
        
class TicketRegisterStrategy(TicketStrategy):
    
    def validate_event_registration(self, event, user):
        """Validate conditions for event registration."""
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
    
    def execute(self,request ,id):
        user = request.user
        event = get_object_or_404(Event, id= id)
        
        try: 
            self.validate_event_registration(event, user)
        except ValidationError as e:
            return Response({'error': e.messages[0]}, status=400)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=403)
        
        ticket = Ticket(
            event=event,
            attendee=user,
            register_date=timezone.now(),
            status='ACTIVE',
            created_at=timezone.now(),
        )
        
        if not ticket.is_valid_min_age_requirement():
            return Response({
                'error': f"You must be at least {event.min_age_requirement} years old to attend this event."
            }, status = 400)
            
        try:
            ticket.clean()
            ticket.save()
            
            notification_manager = TicketNotificationManager(ticket)
            notification_manager.send_registration_confirmation()
            return Response(TicketResponseSchema(
                **ticket.get_ticket_details()).dict(), status=201)
                
        except ValidationError as e:
            return Response({'error': str(e.messages[0])}, status=400)
        except Exception as e:
            logger.error(f"Error during ticket registration: {str(e)}")
            return Response({'error': 'Internal server error'}, status=500)


class TicketDeleteStrategy(TicketStrategy):
    
    def execute(self, request, ticket_id):
        this_user = request.user
        try:
            ticket = Ticket.objects.get(id=ticket_id, attendee=this_user)
            # Send cancellation email before deleting the ticket
            try:
                notification_manager = TicketNotificationManager(ticket)
                notification_manager.send_cancellation_notification()
            except Exception as email_error:
                logger.error(f"Failed to send cancellation email: {str(email_error)}")
                return Response({'error': 'Failed to send cancellation email'}, status=500)
            
            ticket.delete()
            return Response({
                "success": f"Ticket with ID {ticket_id} has been canceled."
            }, status=200)
            
        except Ticket.DoesNotExist:
            logger.error(f"Ticket with ID {ticket_id} does not exist or belongs to a different user.")
            return Response({
                "error": f"Ticket with ID {ticket_id} does not exist or you do not have permission to cancel it."
            }, status=404)
        except Exception as e:
            logger.error(f"Error during ticket cancellation: {str(e)}")
            return Response({'error': 'Internal server error'}, status=500)
        
        
class TicketSendReminderStrategy(TicketStrategy):
    
    def execute(self, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.email_sent = True
        ticket.save()
        ticket.send_event_reminder()
        