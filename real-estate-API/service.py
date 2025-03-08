from django.core.exceptions import ValidationError
from .models import General_Info
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
    return General_Info.objects.create(
        username=username,
        password=password,
        email_address=email_address,
        location=location,
        is_agent=is_agent,
    )


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
