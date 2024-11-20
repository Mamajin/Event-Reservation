from django.urls import path
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from api.views.user import UserAPI
from api.views.event import EventAPI
from api.views.ticket import TicketAPI
from api.views.bookmarks import BookmarkAPI
from api.views.like import LikeAPI
from api.views.comment import CommentAPI
from api.views.organizer import OrganizerAPI
from django.conf import settings
from django.conf.urls.static import static

api = NinjaExtraAPI(version ="2.0.0", urls_namespace= "api")
api.register_controllers(NinjaJWTDefaultController)
api.register_controllers(UserAPI)
api.register_controllers(EventAPI)
api.register_controllers(OrganizerAPI)
api.register_controllers(TicketAPI)
api.register_controllers(LikeAPI)
api.register_controllers(CommentAPI)
api.register_controllers(BookmarkAPI)

urlpatterns = [
    path("", api.urls),  # Prefix all API routes with /api/
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
