from django.urls import path
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from api.views.user import router as user_router
from api.views.organizer import router as organizer_router
from api.views.event import router as event_router
from api.views.ticket import router as ticket_router
from api.views.session import router as session_router
from django.conf import settings
from django.conf.urls.static import static
# from api.views.google_login import router as google_login

api = NinjaExtraAPI(version ="2.0.0")
api.register_controllers(NinjaJWTDefaultController)

# Register routers for different models/views
api.add_router("/users/", user_router)
api.add_router("/organizers/", organizer_router)
api.add_router("/events/", event_router)
api.add_router("/tickets/", ticket_router)
api.add_router("/sessions/", session_router)

urlpatterns = [
    path("", api.urls),  # Prefix all API routes with /api/
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
