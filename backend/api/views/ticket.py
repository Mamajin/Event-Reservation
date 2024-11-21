from api.views.schemas.ticket_schema import TicketResponseSchema
from api.views.schemas.other_schema import ErrorResponseSchema
from .modules import *
from .strategy.ticket_strategy import *


     
@api_controller("/tickets/", tags=["Tickets"])
class TicketAPI:
    """
    Controller for handling ticket-related operations.
    """
    @route.get('/user/{user_id}', response=List[TicketResponseSchema], auth=JWTAuth())
    def list_user_tickets(self, request: HttpRequest, user_id: int):
        """
        Retrieve a list of tickets for a specific user.

        Args:
            request (HttpRequest): The HTTP request object, containing user and request metadata.
            user_id (int): The ID of the user for whom the ticket list is requested.

        Returns:
            List[TicketResponseSchema]: A list of tickets associated with the user.
        """
        strategy : TicketStrategy = TicketStrategy.get_strategy("get_user_ticket")
        return strategy.execute(user_id)
            

    @route.post('/event/{event_id}/register', response={201: TicketResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())
    def register_for_event(self,request: HttpRequest, event_id: int):
        """
        Register a user for an event.

        Args:
            request (HttpRequest): The HTTP request object, containing user and request metadata.
            event_id (int): The ID of the event for which the user is registering.

        Returns:
            TicketResponseSchema: A TicketResponseSchema object containing details of the newly created ticket.

        Raises:
            400: If event registration is not allowed or if the user is already registered for the event.
        """

        strategy : TicketStrategy = TicketStrategy.get_strategy('register_ticket')
        return strategy.execute(request, event_id)
        

    @route.delete('/{ticket_id}/cancel', auth=JWTAuth())
    def cancel_ticket(self,request: HttpRequest, ticket_id: int):
        """
        Cancel a ticket for a specific user.

        Args:
            request (HttpRequest): The HTTP request object, containing user and request metadata.
            ticket_id (int): The ID of the ticket to be canceled.

        Returns:
            Response: A response indicating the success or failure of the ticket cancellation.

        Raises:
            404: If the ticket does not exist or the user does not have permission to cancel it.
            500: If there is an error during the cancellation process.
        """
        strategy : TicketStrategy = TicketStrategy.get_strategy('cancel_ticket')
        return strategy.execute(request, ticket_id)
        
    @route.get('/{ticket_id}', response=TicketResponseSchema, auth=JWTAuth())
    def ticket_detail(self,request: HttpRequest, ticket_id: int):
        """
        Retrieve detailed information for a specific ticket.

        Args:
            request (HttpRequest): The HTTP request object, containing user and request metadata.
            ticket_id (int): The ID of the ticket for which details are requested.

        Returns:
            TicketResponseSchema: A TicketResponseSchema object containing detailed information about the ticket.

        Raises:
            404: If the ticket does not exist.
            500: If there is an error during the retrieval process.
        """
        strategy : TicketStrategy = TicketStrategy.get_strategy('get_ticket_detail')
        return strategy.execute(ticket_id)

    @route.post('/{ticket_id}/send-reminder', auth=JWTAuth())
    def send_remider(self,request: HttpRequest, ticket_id: int):
        """
        Send a reminder email to a specific ticket holder.

        Args:
            request (HttpRequest): The HTTP request object, containing user and request metadata.
            ticket_id (int): The ID of the ticket for which the reminder email is requested.

        Returns:
            Response: A response indicating the success or failure of the reminder email sent.

        Raises:
            404: If the ticket does not exist or the user does not have permission to send a reminder.
            500: If there is an error during the sending process.
        """
        startegy : TicketStrategy = TicketStrategy.get_strategy('sent_reminder')
        return startegy.execute(ticket_id)
        