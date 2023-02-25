from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegisterationSerializer(serializers.ModelSerializer):
    """
    A class to serialize user details for new user creation.
    With a function called create to actually create user.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create a new user and return created user object
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    """
    A class to serialize user details for login a user.
    """
    # Will validate Username
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ["username", "password"]