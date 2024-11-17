from django.urls import path
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from api.views.user import router as user_router
from api.views.organizer import router as organizer_router
from api.views.event import router as event_router
from api.views.ticket import TicketAPI
from api.views.bookmarks import router as bookmark_router
from api.views.like import router as like_router
from api.views.comment import router as comment_router
from api.views.organizer import OrganizerAPI
from django.conf import settings
from django.conf.urls.static import static

api = NinjaExtraAPI(version ="2.0.0", urls_namespace= "api")
api.register_controllers(NinjaJWTDefaultController)
api.register_controllers(OrganizerAPI)
api.register_controllers(TicketAPI)

# Register routers for different models/views
api.add_router("/users/", user_router)
api.add_router("/organizers/", organizer_router)
api.add_router("/events/", event_router)
api.add_router('/bookmarks/', bookmark_router)
api.add_router('/likes/', like_router)
api.add_router('/comments', comment_router)

urlpatterns = [
    path("", api.urls),  # Prefix all API routes with /api/
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
