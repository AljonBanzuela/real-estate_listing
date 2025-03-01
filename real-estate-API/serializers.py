from rest_framework import serializers
from .models import General_Info


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = General_Info
        field = ['username', 'password', 'email_address', 'location', 'is_agent']



