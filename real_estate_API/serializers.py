from rest_framework import serializers
from .models import General_Info, Regular_User, Agent_User, Property_Description, Feedback, Images, Property_Price, \
    PaymentRecord, PropertyNotification


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
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
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
        fields = ['id', 'general_info', 'username', 'lot_size_ideal', 'room_no_ideal', 'floor_no_ideal',
                  'location_ideal',
                  'price_rent_ideal', 'price_full_ideal']

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
        fields = ['id', 'general_info', 'agent_description', 'years_of_exp', 'is_available']

    def create(self, validated_data):
        general_info_data = validated_data.pop('general_info')
        general_info = General_Info.objects.create(**general_info_data)
        agent_user = Agent_User.objects.create(general_info=general_info, **validated_data)
        return agent_user

    def update(self, instance, validated_data):
        general_info_data = validated_data.pop('general_info')
        instance.agent_description = validated_data.get('agent_description', instance.description_agent)
        instance.years_of_exp = validated_data.get('years_of_exp', instance.years_of_exp)
        instance.is_available = validated_data.get('is_available', instance.is_available)
        general_info_data = validated_data.pop('general_info', None)
        if general_info_data:
            general_info_serializer = GeneralInfoSerializer(instance.general_info, data=general_info_data)
            if general_info_serializer.is_valid():
                general_info_serializer.save()
        instance.save()
        return instance


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'comment', 'rating', 'created_at']


class PropertySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    sample_image = serializers.SerializerMethodField()  # Field for the sample image
    current_price = serializers.SerializerMethodField()

    class Meta:
        model = Property_Description
        fields = ['id', 'prop_name', 'lot_size', 'room_no', 'floor_no', 'location', 'is_full', 'is_rent',
                  'sample_image', 'current_price']

    @staticmethod
    def get_prices(obj):
        price = obj.prices.last()
        if price:
            return {
                'current_rent_price': price.price_rent,
                'current_full_price': price.price_full,
                'upcoming_rent_price': price.price_rent_next,
                'upcoming_full_price': price.price_full_next,
            }
        return None

    @staticmethod
    def get_sample_image(obj):
        image = obj.images.first()
        return image.exterior.url if image and image.exterior else None

    @staticmethod
    def get_current_price(obj):
        price = obj.prices.last()
        if price:
            if obj.is_full:
                return price.price_full  # Use full payment price
            elif obj.is_rent:
                return price.price_rent  # Use rent price
        return None


class PropertyPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property_Price
        fields = ('id', 'price_rent', 'price_full', 'price_rent_next', 'price_full_next')


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['exterior', 'interior', 'floor_plan']


class PaymentMethodSerializer(serializers.ModelSerializer):
    rent_duration_months = serializers.SerializerMethodField()

    class Meta:
        model = Property_Price
        fields = ['price_rent', 'price_full', 'rent_duration_months']

    @staticmethod
    def get_rent_duration_months(obj):
        # Only include rent_duration_months if the property is for rent
        if obj.property_description.is_rent:
            return obj.rent_duration_months
        return None


class PaymentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRecord
        fields = ['id', 'amount', 'due_date', 'payment_date', 'status']


class PropertyNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyNotification
        fields = ['id', 'user', 'property', 'message', 'is_read', 'created_at']
        depth = 1
