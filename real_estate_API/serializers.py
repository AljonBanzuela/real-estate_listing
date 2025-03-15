from rest_framework import serializers
from .models import General_Info, Regular_User, Agent_User


class GeneralInfoSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = General_Info
        fields = ['id', 'username', 'password', 'email_address', 'location', 'is_agent', 'created_at']

    def create(self, validated_data):
        general_info = General_Info(
            username=validated_data['username'],
            email_address=validated_data['email_address'],
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


class RegularUserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(source='general_info.username', read_only=True)  # Include username
    general_info = GeneralInfoSerializer()

    class Meta:
        model = Regular_User
        fields = ['id', 'general_info', 'lot_size_ideal', 'room_no_ideal', 'floor_no_ideal', 'location_ideal', 'price_rent_ideal', 'price_full_ideal']

    def create(self, validated_data):
        general_info_data = validated_data.pop('general_info')
        general_info = General_Info.objects.create(**general_info_data)
        regular_user = Regular_User.objects.create(general_info=general_info, **validated_data)
        return regular_user

    def update(self, instance, validated_data):
        general_info_data = validated_data.pop('general_info')
        instance.lot_size_ideal = validated_data.get('lot_size_ideal', instance.lot_size_ideal)
        instance.room_no_ideal = validated_data.get('room_no_ideal', instance.room_no_ideal)
        instance.floor_no_ideal = validated_data.get('floor_no_ideal', instance.floor_no_ideal)
        instance.location_ideal = validated_data.get('location_ideal', instance.location_ideal)
        instance.price_rent_ideal = validated_data.get('price_rent_ideal', instance.price_rent_ideal)
        instance.price_full_ideal = validated_data.get('price_full_ideal', instance.price_full_ideal)

        general_info_serializer = GeneralInfoSerializer(instance.general_info, data=general_info_data)
        if general_info_serializer.is_valid():
            general_info_serializer.save()
        instance.save()
        return instance


class AgentUserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(source='general_info.username', read_only=True)  # Include username
    general_info = GeneralInfoSerializer()

    class Meta:
        model = Agent_User
        fields = ['id', 'general_info', 'description_agent', 'years_of_exp', 'is_available']

    def create(self, validated_data):
        general_info_data = validated_data.pop('general_info')
        general_info = General_Info.objects.create(**general_info_data)
        agent_user = Agent_User.objects.create(general_info=general_info, **validated_data)
        return agent_user

    def update(self, instance, validated_data):
        general_info_data = validated_data.pop('general_info')
        instance.description_agent = validated_data.get('description_agent', instance.description_agent)
        instance.years_of_exp = validated_data.get('years_of_exp', instance.years_of_exp)
        instance.is_available = validated_data.get('is_available', instance.is_available)

        general_info_serializer = GeneralInfoSerializer(instance.general_info, data=general_info_data)
        if general_info_serializer.is_valid():
            general_info_serializer.save()
        instance.save()
        return instance
