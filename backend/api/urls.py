from django.urls import path
from api.views import CreateUserView, CreateOrganizerView, CreateEventView

urlpatterns = [
    path("create-event/", CreateEventView.as_view(), name='create-event'),
]
