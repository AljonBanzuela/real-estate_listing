from django.core.exceptions import ObjectDoesNotExist
from .models import (General_Info, Regular_User, Agent_User, Property_Description,
                     Images, Feedback, Property_Price, Request, PaymentRecord, PropertyNotification)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Avg, Q
from datetime import date, timedelta


def get_user_list():
    return General_Info.objects.all().order_by("-created_at")


def get_user_by_id(pk):
    try:
        return General_Info.objects.get(pk=pk)
    except General_Info.DoesNotExist:
        return None


def create_user(username, password, email_address, location, is_agent=False):
    if General_Info.objects.filter(email_address=email_address).exists():
        raise ValueError('A user with this email address already exists')
    user = General_Info.objects.create(
        username=username,
        email_address=email_address,
        location=location,
        is_agent=is_agent
    )
    user.set_password(password)
    user.save()
    return user


def update_user_by_id(pk, data):
    general_info = get_user_by_id(pk)
    if general_info:
        for key, value in data.items():
            setattr(general_info, key, value)
        general_info.save()
    return general_info


def delete_user_by_id(pk):
    general_info = get_user_by_id(pk)
    if general_info:
        general_info.delete()
    return general_info


def login_user(email, password):
    general_info = authenticate(email=email, password=password)
    if general_info:
        refresh = RefreshToken.for_user(general_info)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    return general_info


def get_user_preference(user_id):
    try:
        return Regular_User.objects.get(general_info__id=user_id)
    except Regular_User.DoesNotExist:
        return None


def create_user_preference(user_id, data):
    try:
        user_info = General_Info.objects.get(id=user_id)
        preference = Regular_User.objects.create(general_info=user_info, **data)
        preference.save()
        return preference
    except General_Info.DoesNotExist:
        return None


def update_user_preference(user_id, data):
    try:
        preference = Regular_User.objects.get(general_info__id=user_id)
        for key, value in data.items():
            setattr(preference, key, value)
        preference.save()
        return preference
    except Regular_User.DoesNotExist:
        return None


def delete_user_preference(user_id):
    try:
        preference = Regular_User.objects.get(general_info__id=user_id)
        preference.delete()
        return preference
    except Regular_User.DoesNotExist:
        return None


def get_agent_details(agent_id):
    try:
        return Agent_User.objects.get(general_info__id=agent_id)
    except Agent_User.DoesNotExist:
        return None


def create_agent_details(agent_id, data):
    try:
        agent_info = General_Info.objects.get(id=agent_id)
        details = Agent_User.objects.create(general_info=agent_info, **data)
        details.save()
        return details
    except General_Info.DoesNotExist:
        return None


def update_agent_details(agent_id, data):
    try:
        details = Agent_User.objects.get(general_info__id=agent_id)
        for key, value in data.items():
            setattr(details, key, value)
        details.save()
        return details
    except Agent_User.DoesNotExist:
        return None


def delete_agent_details(agent_id):
    try:
        details = Agent_User.objects.get(general_info__id=agent_id)
        details.delete()
        return details
    except Agent_User.DoesNotExist:
        return None


def get_all_properties():
    return Property_Description.objects.all()


def get_property_by_id(property_id):
    try:
        return Property_Description.objects.get(id=property_id)
    except Property_Description.DoesNotExist:
        return None


def create_property(data):
    property_description = Property_Description.objects.create(**data)
    property_description.save()
    return property_description


def update_property_by_id(property_id, data):
    property_description = get_property_by_id(property_id)
    if property_description:
        for key, value in data.items():
            setattr(property_description, key, value)
        property_description.save()
    return property_description


def delete_property_by_id(property_id):
    property_description = get_property_by_id(property_id)
    if property_description:
        property_description.delete()
    return property_description


def get_property_visuals(property_id):
    try:
        property_description = get_property_by_id(property_id)
        if property_description:
            visuals = property_description.images.all()  # Related images
            return visuals
        return None
    except ObjectDoesNotExist:
        return None


def get_property_price(property_id):
    try:
        # Fetch the property object
        property_description = get_property_by_id(property_id)
        if property_description:
            # Access the latest price using the 'prices' related name
            price = property_description.prices.last()
            if price:
                return {
                    'current_rent_price': price.price_rent,
                    'current_full_price': price.price_full,
                    'upcoming_rent_price': price.price_rent_next,
                    'upcoming_full_price': price.price_full_next
                }
        return None
    except ObjectDoesNotExist:
        return None


def calculate_average_rating(property_id):
    try:
        property_description = get_property_by_id(property_id)
        if property_description:
            # Use aggregate to calculate the average rating
            average_rating = \
                Feedback.objects.filter(property_description=property_description).aggregate(Avg('rating'))[
                    'rating__avg']
            return round(average_rating, 2) if average_rating is not None else 0
        return None
    except Property_Description.DoesNotExist:
        return None


def create_property_request(user_id, property_id):
    """
    Create a request for the selected property to purchase/rent.
    """
    try:
        user = General_Info.objects.get(pk=user_id)
        property_description = Property_Description.objects.get(pk=property_id)
        # Check if the request already exists
        if Request.objects.filter(user=user, property_description=property_description).exists():
            raise ValueError("Request already exists for this property.")

        # Create and save the new request
        new_request = Request.objects.create(
            user=user,
            property_description=property_description
        )
        return new_request
    except General_Info.DoesNotExist:
        raise ObjectDoesNotExist("User not found.")
    except Property_Description.DoesNotExist:
        raise ObjectDoesNotExist("Property not found.")


def assign_agent_to_request(user_id, property_id, agent_id):
    try:
        user = General_Info.objects.get(pk=user_id)
        property_description = Property_Description.objects.get(pk=property_id)
        agent = Agent_User.objects.get(general_info__id=agent_id)  # Ensure this is an agent

        # Fetch the existing request
        request = Request.objects.filter(user=user, property_description=property_description).first()
        if not request:
            raise ValueError("Request for this property does not exist.")

        # Assign the agent to the request
        request.agent = agent
        request.save()
        return request
    except General_Info.DoesNotExist:
        raise ObjectDoesNotExist("User not found.")
    except Property_Description.DoesNotExist:
        raise ObjectDoesNotExist("Property not found.")
    except Agent_User.DoesNotExist:
        raise ObjectDoesNotExist("Agent not found.")


def get_payment_methods(property_id):
    try:
        property_description = Property_Description.objects.get(pk=property_id)
        price = property_description.prices.last()
        if price:
            return price
        return None
    except Property_Description.DoesNotExist:
        raise ValueError("Property not found.")


def add_payment_method(property_id, rent_price, full_price, rent_duration_months=None):
    try:
        property_description = Property_Description.objects.get(pk=property_id)
        payment = Property_Price.objects.create(
            property_description=property_description,
            price_rent=rent_price,
            price_full=full_price,
            rent_duration_months=rent_duration_months if property_description.is_rent else None
        )
        return payment
    except Property_Description.DoesNotExist:
        raise ValueError("Property not found.")


def search_properties(description=None, min_price=None, max_price=None):
    filters = Q()
    if description:
        filters &= Q(prop_name__icontains=description)  # Case-insensitive partial match on description
    if min_price:
        filters &= Q(prices__price_full__gte=min_price)  # Filter properties with price_full >= min_price
    if max_price:
        filters &= Q(prices__price_full__lte=max_price)  # Filter properties with price_full <= max_price

    # Query filtered properties and ensure unique results
    properties = Property_Description.objects.filter(filters).distinct()
    return properties


def recommend_properties(user_id):
    try:
        # Fetch user preferences
        user_preferences = Regular_User.objects.get(general_info__id=user_id)

        # Filter properties based on user preferences
        recommended_properties = Property_Description.objects.filter(
            lot_size__gte=user_preferences.lot_size_ideal,
            room_no__gte=user_preferences.room_no_ideal,
            location__icontains=user_preferences.location_ideal,  # Case-insensitive partial match
            prices__price_full__lte=user_preferences.price_full_ideal,  # Filter by max full price
            prices__price_rent__lte=user_preferences.price_rent_ideal  # Filter by max rent price
        ).distinct()

        return recommended_properties
    except Regular_User.DoesNotExist:
        raise ValueError("User preferences not found.")


def get_upcoming_payments(user_id):
    today = date.today()
    upcoming_payments = PaymentRecord.objects.filter(
        user__id=user_id,
        status='pending',
        due_date__lte=today + timedelta(days=7)  # Payments due in the next 7 days
    )
    return upcoming_payments


def get_payment_records(user_id):
    payment_records = PaymentRecord.objects.filter(user__id=user_id).order_by('-due_date')
    return payment_records


def calculate_payments_left(user_id, property_id):
    pending_payments = PaymentRecord.objects.filter(
        user__id=user_id,
        property__id=property_id,
        status='pending'
    )
    return pending_payments.count()

def compare_properties_with_payment(property_id_1, property_id_2):
    try:
        # Fetch properties
        property_1 = Property_Description.objects.get(pk=property_id_1)
        property_2 = Property_Description.objects.get(pk=property_id_2)

        # Fetch latest payment details for each property
        payment_1 = property_1.prices.last()  # Retrieve the latest price record for property 1
        payment_2 = property_2.prices.last()  # Retrieve the latest price record for property 2

        # Organize comparison data, including payment information
        comparison_data = {
            'property_1': {
                'name': property_1.prop_name,
                'lot_size': property_1.lot_size,
                'room_no': property_1.room_no,
                'floor_no': property_1.floor_no,
                'location': property_1.location,
                'is_full': property_1.is_full,
                'is_rent': property_1.is_rent,
                'payment': {
                    'current_rent_price': payment_1.price_rent if payment_1 else None,
                    'current_full_price': payment_1.price_full if payment_1 else None,
                    'upcoming_rent_price': payment_1.price_rent_next if payment_1 else None,
                    'upcoming_full_price': payment_1.price_full_next if payment_1 else None,
                }
            },
            'property_2': {
                'name': property_2.prop_name,
                'lot_size': property_2.lot_size,
                'room_no': property_2.room_no,
                'floor_no': property_2.floor_no,
                'location': property_2.location,
                'is_full': property_2.is_full,
                'is_rent': property_2.is_rent,
                'payment': {
                    'current_rent_price': payment_2.price_rent if payment_2 else None,
                    'current_full_price': payment_2.price_full if payment_2 else None,
                    'upcoming_rent_price': payment_2.price_rent_next if payment_2 else None,
                    'upcoming_full_price': payment_2.price_full_next if payment_2 else None,
                }
            }
        }
        return comparison_data

    except Property_Description.DoesNotExist:
        raise ValueError("One or both properties do not exist.")


def notify_new_deal(property_id):
    try:
        # Fetch the property that was just added
        new_property = Property_Description.objects.get(pk=property_id)
        users = General_Info.objects.all()  # Notify all users

        notifications = []
        for user in users:
            notifications.append(PropertyNotification(
                user=user,
                property=new_property,
                message=f"A new property deal is available: {new_property.prop_name}"
            ))

        # Bulk create notifications for better efficiency
        PropertyNotification.objects.bulk_create(notifications)
        return notifications
    except Property_Description.DoesNotExist:
        raise ValueError("Property does not exist.")


def notify_property_request_approval(property_id):
    try:
        # Fetch the approved request
        approved_request = Request.objects.filter(
            property_description__id=property_id,
            status='approved'
        ).first()

        if not approved_request:
            raise ValueError("No approved request found for this property.")

        # Notify the user about the approval
        notification = PropertyNotification.objects.create(
            user=approved_request.user,
            property=approved_request.property_description,
            message=f"Your request for {approved_request.property_description.prop_name} has been accepted by an agent."
        )
        return notification
    except Request.DoesNotExist:
        raise ValueError("The request or property does not exist.")
