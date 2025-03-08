from rest_framework import serializers
from .models import General_Info


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = General_Info
        field = ['username', 'password', 'email_address', 'location', 'is_agent']

    def create(self, validated_data):
        general_info = General_Info(
            username=validated_data['username'],
            email=validated_data['email'],
            location=validated_data['location'],
            is_agent=validated_data['is_agent']
        )
        general_info.set_password(validated_data['password'])
        general_info.save()
        return general_info

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.location = validated_data.get('location', instance.location)
        instance.is_agent = validated_data.get('is_agent', instance.is_agent)
        instance.save()
        return instance
