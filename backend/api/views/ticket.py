from .modules import List, JWTAuth, get_object_or_404, Ticket, AttendeeUser, Event, Router
from .schemas import TicketSchema

router = Router()


class TicketAPI:
    
    @router.get('event/{user_id}', response=List[TicketSchema], auth = JWTAuth())
    def list_event(request, user_id: int):
        user = get_object_or_404(AttendeeUser, id = user_id)
        return user.ticket_set.all()
        
        
    @router.post('event/{event_id}/reserve', response= TicketSchema, auth= JWTAuth())
    def event_reserve(request, event_id):
        user_id = request.user.id
        event = get_object_or_404(Event, id = event_id)
        user = get_object_or_404(AttendeeUser, id = user_id)
        ticket = Ticket.objects.create(event = event, attendee = user)
        return ticket
    
    @router.delete('delete-event/{ticket_id}', auth= JWTAuth())
    def delete_event(request, ticket_id):
        this_user = request.user
        try:
            ticket = this_user.ticket_set.get(id = ticket_id)
        except Ticket.DoesNotExist:
            return {"error": f"This ticket is does not exist."}
        ticket.delete()
        return {"success": f"Ticket with ID {ticket.id} has been canceled."}