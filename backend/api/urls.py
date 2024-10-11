from django.urls import path
from api.views import CreateUserView, OrganizerDetailView

urlpatterns = [
    path("organizers/", OrganizerDetailView.as_view(), name='organizer-detail'),
]
