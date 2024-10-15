from django.urls import path
from ninja import NinjaAPI
from api.views.user import router as user_router
from api.views.organizer import router as organizer_router
from api.views.event import router as event_router
from api.views.attendee import router as attendee_router
from api.views.ticket import router as ticket_router

api = NinjaAPI(version ="2.0.0")

# Register routers for different models/views
api.add_router("/users/", user_router)
api.add_router("/organizers/", organizer_router)
api.add_router("/events/", event_router)
api.add_router("/attendees/", attendee_router)
api.add_router("/tickets/", ticket_router)

urlpatterns = [
    path("", api.urls),  # Prefix all API routes with /api/
]
