from django.urls import path
from .views import register_view, login_view, general_info_list_view, general_info_detail_view, user_preference_view,agent_details_view

urlpatterns = [
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('general-info/', general_info_list_view, name='general_info_list'),
    path('general-info/<int:pk>/', general_info_detail_view, name='general_info_detail'),
    path('user/<int:user_id>/preference/', user_preference_view, name='user_preference'),
    path('agent/<int:agent_id>/details/', agent_details_view, name='agent_details'),
]
