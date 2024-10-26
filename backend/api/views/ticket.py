from .modules import List, JWTAuth, get_object_or_404, Ticket, AttendeeUser, Event, Router, Response, logger, Organizer
from .schemas import TicketSchema

router = Router()


class TicketAPI:
    
    @router.get('event/{user_id}', response=List[TicketSchema], auth = JWTAuth())
    def list_event(request, user_id: int):
        try:
            user = AttendeeUser.objects.get(id = user_id)
        except AttendeeUser.DoesNotExist:
            return Response({'error': 'This user does not exists'}, status = 400)

        return user.ticket_set.all()
        
        
    @router.post('event/{event_id}/reserve', response= TicketSchema, auth= JWTAuth())
    def event_reserve(request, event_id):
        user_id = request.user.id
        try:
            event = Event.objects.get(id = event_id)
        except Event.DoesNotExist:
            logger.error('This event does not exist')
            return Response({'error': 'This event does not exists'}, status = 404)
        try:
            user = AttendeeUser.objects.get(id = user_id)
        except AttendeeUser.DoesNotExist:
            logger.error('This user does not exists')
            return Response({'error': 'This user does not exists'}, status = 404)
        
        if Ticket.objects.filter(attendee = user, event = event).exists():
            return Response({'error': 'You have registered this event already'}, status = 400)
        
        if Organizer.objects.filter(user = request.user).exists():
            organizer = Organizer.objects.get(user = request.user)
            if event.organizer == organizer:
                return Response({'error': 'Organizer is not allowed to register own event.'}, status = 400)
            
        if event.is_max_attendee():
            return Response({'error': "This event is full"}, status = 400)

        elif event.can_register():
            ticket = Ticket.objects.create(event = event, attendee = user)
            return ticket
        
        else:
            return Response({'error': 'Registration for this event is not allowed.'}, status = 400)
        

    
    @router.delete('delete-event/{ticket_id}', auth= JWTAuth())
    def delete_event(request, ticket_id):
        this_user = request.user
        try:
            ticket = this_user.ticket_set.get(id = ticket_id)
        except Ticket.DoesNotExist:
            return Response({"error": f"This ticket is does not exist."}, status = 400)
        ticket.delete()
        return Response({"success": f"Ticket with ID {ticket_id} has been canceled."}, status = 200)