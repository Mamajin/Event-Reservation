from .modules import List, JWTAuth, get_object_or_404, Ticket, AttendeeUser, Event, Router, Response, logger, timezone, HttpRequest
from .schemas import TicketSchema, TicketResponseSchema, SessionSchema, SessionResponseSchema, ErrorResponseSchema

router = Router()

class TicketAPI:
    
    @router.get('/user/{user_id}', response=List[TicketResponseSchema], auth=JWTAuth())
    def list_user_tickets(request: HttpRequest, user_id: int):
        try:
            user = AttendeeUser.objects.get(id=user_id)
            tickets = Ticket.objects.filter(attendee=user, register_date__lte=timezone.now()).order_by("-register_date")
            return [TicketResponseSchema(
                id=ticket.id,
                ticket_number=ticket.ticket_number,
                event_id=ticket.event.id,
                user_id=ticket.attendee.id,
                register_date=ticket.register_date,
                status=ticket.status
                   )
                    for ticket in tickets]
        except AttendeeUser.DoesNotExist:
            logger.error(f"User with ID {user_id} does not exist.")
            return Response({'error': 'User not found'}, status=404)

    @router.post('/event/{event_id}/register', response=TicketResponseSchema, auth=JWTAuth())
    def register_for_event(request: HttpRequest, event_id: int):
        user = request.user
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            logger.error(f"Event with ID {event_id} does not exist.")
            return Response({'error': 'Event not found'}, status=404)
                
        ticket = Ticket(
            event=event,
            attendee=user,
            register_date=timezone.now()
        )
        
        if ticket.is_user_registered(user):
            return Response({'error': 'You have already registered for this event'}, status=400)
        
        if ticket.is_organizer_join_own_event(user):
            return Response({'error': 'Organizer is not allowed to register for their own event'}, status=400)
            
        if event.is_max_attendee():
            return Response({'error': "This event has reached the maximum number of attendees"}, status=400)

        if event.can_register():
            ticket_number = ticket.generate_ticket_number()
            ticket.save()
            return TicketResponseSchema(
                id=ticket.id,
                ticket_number=ticket_number,
                event_id=event_id,
                user_id=user.id,
                register_date=ticket.register_date,
                status='ACTIVE'
            )
        else:
            return Response({'error': 'Registration for this event is not allowed'}, status=400)

    @router.delete('/{ticket_id}/cancel', auth=JWTAuth())
    def cancel_ticket(request: HttpRequest, ticket_id: int):
        this_user = request.user
        try:
            ticket = Ticket.objects.get(id=ticket_id, attendee=this_user)
            ticket.delete()
            return Response({"success": f"Ticket with ID {ticket_id} has been canceled."}, status=200)
        except Ticket.DoesNotExist:
            logger.error(f"Ticket with ID {ticket_id} does not exist or belongs to a different user.")
            return Response({"error": f"Ticket with ID {ticket_id} does not exist or you do not have permission to cancel it."}, status=404)
        
    @router.get('/{ticket_id}', response=TicketResponseSchema, auth=JWTAuth())
    def ticket_detail(request: HttpRequest, ticket_id: int):
        """Get detailed information about a specific ticket.

        Args:
            request (HttpRequest): The HTTP request object
            ticket_id (int): The ID of the ticket to retrieve
        """
        try:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            return Response(TicketResponseSchema(
                id=ticket.id,
                ticket_number=ticket.ticket_number,
                event_id=ticket.event.id,
                user_id=ticket.attendee.id,
                register_date=ticket.register_date,
                status=ticket.status
            ), status=200)
        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=404)
