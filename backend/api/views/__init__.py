from api.views.user import router as user_router
from api.views.event import router as event_router
from api.views.organizer import router as organizer_router
from api.views.ticket import router as ticket_router

__all__ = ['user_router', 'event_router', 
           'organizer_router', 'ticket_router']
