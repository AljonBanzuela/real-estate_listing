from django.core.exceptions import ValidationError
from .models import General_Info


def get_user_list():
    return General_Info.objects.all().order_by("-created_at")


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



def create_todo(name, description=None, status="pending"):
    return Todo.objects.create(
        name=name,
        description=description,
        status=status,
    )
