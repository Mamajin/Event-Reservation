from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
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
