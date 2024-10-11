from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from api.serializers import UserSerializer, OrganizerSerializer, EventSerializer, AttendeeSerializer, TicketSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.models import Organizer, Event, Attendee, Ticket


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class CreateOrganizerView(generics.CreateAPIView):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer
    permission_classes = [IsAuthenticated]
    