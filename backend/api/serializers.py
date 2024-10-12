from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Organizer, Event, Attendee, Ticket


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model, handling user creation and validation, 
    including password confirmation.
    """
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """
        Check that the two passwords match.

        Returns:
            data: The data of user.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        """
        Create a new user with the provided validated data.  

        Returns:
            User: The created User instance.

        Raises:
            serializers.ValidationError: If the username is already taken or any other integrity constraint is violated.
        """
        validated_data.pop('password2')  # Assuming password2 is only for confirmation and not saved
        try:
            user = User.objects.create_user(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"detail": "This username is already taken."})
        return user
    

class OrganizerSerializer(serializers.ModelSerializer):
    """
    Serializer for Organizer model, converting Organizer model instances 
    into JSON and vice versa.
    """
    class Meta:
        model = Organizer
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model, converting Event instances to JSON and 
    managing event-related data.
    """
    organizer = OrganizerSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'event_name', 'organizer', 'event_create_date', 'start_date_event', 
                  'end_date_event', 'start_date_register', 'end_date_register', 
                  'description', 'max_attendee']

    def create(self, validated_data):
        """
        Assign the authenticated organizer to the event.
        """
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            organizer = Organizer.objects.get(user=request.user)
            validated_data['organizer'] = organizer
        return super().create(validated_data)


class AttendeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Attendee model, handling the conversion of Attendee 
    model instances into JSON format.
    """
    class Meta:
        model = Attendee
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for Ticket model, handling ticket-related data, including 
    events and attendees, in a JSON-compatible format.
    """
    event = EventSerializer(read_only=True)
    attendee = AttendeeSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
