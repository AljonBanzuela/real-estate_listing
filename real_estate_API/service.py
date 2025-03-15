from django.core.exceptions import ValidationError
from .models import General_Info, Regular_User, Agent_User, Property_Description, Images, Feedback
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


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
