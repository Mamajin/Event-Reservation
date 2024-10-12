from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from api.serializers import UserSerializer, OrganizerSerializer, EventSerializer, AttendeeSerializer, TicketSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from api.models import Organizer, Event, Attendee, Ticket


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class OrganizerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer


class CreateEventView(generics.CreateAPIView):
    """
    View to allow an Organizer to create an Event.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Overriden to assign the authenticated Organizer to the event.
        """
        user = self.request.user
        try:
            organizer = Organizer.objects.get(user=user)
        except Organizer.DoesNotExist:
            raise PermissionDenied("You must be an organizer.")
        
        serializer.save(organizer=organizer)
