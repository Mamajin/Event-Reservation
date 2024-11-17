from .modules import *
from .schemas import TicketSchema, TicketResponseSchema, SessionSchema, SessionResponseSchema, ErrorResponseSchema

router = Router()

class TicketAPI:
    
    @router.get('/user/{user_id}', response=List[TicketResponseSchema], auth=JWTAuth())
    def list_user_tickets(request: HttpRequest, user_id: int):
        try:
            user = AttendeeUser.objects.get(id=user_id)
            tickets = Ticket.objects.filter(attendee=user, register_date__lte=timezone.now()).order_by("-register_date")
            return [
                TicketResponseSchema(
                    **ticket.get_ticket_details()
                ) for ticket in tickets
            ]
        except AttendeeUser.DoesNotExist:
            logger.error(f"User with ID {user_id} does not exist.")
            return Response({'error': 'User not found'}, status=404)

    @router.post('/event/{event_id}/register', response={201: TicketResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())
    def register_for_event(request: HttpRequest, event_id: int):
        """Register a user for an event and create a ticket."""
        user = request.user
        event = get_object_or_404(Event, id=event_id)
        
        if event.is_max_attendee():
            return Response(
                {'error': "This event has reached the maximum number of attendees"},
                status=400
            )

        if not event.can_register():
            return Response(
                {'error': 'Registration for this event is not allowed'},
                status=400
            )
        if not event.is_registration_status_allowed():
            return Response(
                {'error': f'Registeration of this event is {event.status_registeration.lower()} now'},
                status=400
                ) 
                
        if event.visibility == 'PRIVATE' and not event.is_email_allowed(user.email):
            return Response({
                'error': 'Your email domain is not authorized to register for this event'
            }, status=403)
            
        ticket = Ticket(
            event=event,
            attendee=user,
            register_date=timezone.now(),
            status='ACTIVE',
            created_at=timezone.now(),
        )
        if user.age == None:
            return Response({'error' : "Please set your birth date in accountinfo"}, status = 400)
        
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

    @router.delete('/{ticket_id}/cancel', auth=JWTAuth())
    def cancel_ticket(request: HttpRequest, ticket_id: int):
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
        
    @router.get('/{ticket_id}', response=TicketResponseSchema, auth=JWTAuth())
    def ticket_detail(request: HttpRequest, ticket_id: int):
        """
        Get detailed information about a specific ticket.
        """
        try:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            return Response(TicketResponseSchema(
                **ticket.get_ticket_details()), status=200)
            
        except Http404:
            logger.error(f"Ticket with ID {ticket_id} does not exist.")
            return Response({'error': 'Ticket not found'}, status=404)
        except Exception as e:
            logger.error(f"Error fetching ticket details: {str(e)}")
            return Response({'error': 'Internal server error'}, status=500)

    @router.post('/{ticket_id}/send-reminder', auth=JWTAuth())
    def send_remider(request: HttpRequest, ticket_id: int):
        """Send an event remider after registration."""
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.email_sent = True
        ticket.save()
        ticket.send_event_reminder()
        