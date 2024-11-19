from api.views.schemas.ticket_schema import TicketResponseSchema
from api.views.schemas.other_schema import ErrorResponseSchema
from .modules import *
from .strategy.ticket_strategy import *


     
@api_controller("/tickets/", tags=["Tickets"])
class TicketAPI:
    
    @route.get('/user/{user_id}', response=List[TicketResponseSchema], auth=JWTAuth())
    def list_user_tickets(self, request: HttpRequest, user_id: int):
        strategy : TicketStrategy = TicketStrategy.get_strategy("get_user_ticket")
        return strategy.execute(user_id)
            

    @route.post('/event/{event_id}/register', response={201: TicketResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())
    def register_for_event(self,request: HttpRequest, event_id: int):
        """Register a user for an event and create a ticket."""
        strategy : TicketStrategy = TicketStrategy.get_strategy('register_ticket')
        return strategy.execute(request, event_id)
        

    @route.delete('/{ticket_id}/cancel', auth=JWTAuth())
    def cancel_ticket(self,request: HttpRequest, ticket_id: int):
        strategy : TicketStrategy = TicketStrategy.get_strategy('cancel_ticket')
        return strategy.execute(request, ticket_id)
        
    @route.get('/{ticket_id}', response=TicketResponseSchema, auth=JWTAuth())
    def ticket_detail(self,request: HttpRequest, ticket_id: int):
        """
        Get detailed information about a specific ticket.
        """
        strategy : TicketStrategy = TicketStrategy.get_strategy('get_ticket_detail')
        return strategy.execute(ticket_id)

    @route.post('/{ticket_id}/send-reminder', auth=JWTAuth())
    def send_remider(self,request: HttpRequest, ticket_id: int):
        """Send an event remider after registration."""
        startegy : TicketStrategy = TicketStrategy.get_strategy('sent_reminder')
        return startegy.execute(ticket_id)
        