from django.urls import path
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from api.views.user import UserAPI
from api.views.organizer import router as organizer_router
from api.views.event import EventAPI
from api.views.ticket import TicketAPI
from api.views.bookmarks import router as bookmark_router
from api.views.like import LikeAPI
from api.views.comment import CommentAPI
from django.conf import settings
from django.conf.urls.static import static

api = NinjaExtraAPI(version ="2.0.0", urls_namespace= "api")
api.register_controllers(NinjaJWTDefaultController)
api.register_controllers(TicketAPI)
api.register_controllers(UserAPI)
api.register_controllers(LikeAPI)
api.register_controllers(CommentAPI)
api.register_controllers(EventAPI)



# Register routers for different models/views

api.add_router("/organizers/", organizer_router)
api.add_router('/bookmarks/', bookmark_router)

urlpatterns = [
    path("", api.urls),  # Prefix all API routes with /api/
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
