from django.urls import path
from api.views import CreateUserView, OrganizerDetailView

urlpatterns = [
    path("organizers/<int:pk>", OrganizerDetailView.as_view(), name='organizer-detail'),
]
