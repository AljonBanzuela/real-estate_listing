from django.urls import path
from .views import register_view, login_view

urlpatterns = [
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
]
