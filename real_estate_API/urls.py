from django.urls import path
from .views import (register_view, login_view, general_info_list_view,
                    general_info_detail_view, user_preference_view, agent_details_view,
                    property_list_view, property_detail_view, property_price_view, property_visuals_view,
                    property_review_view, property_request_view, property_request_agent_view, property_payment_method_view,
                    property_search_view, property_recommendation_view, rent_notification_view, rent_record_view,
                    property_comparison_view, alert_new_deal_view, alert_property_request_approval_view)

urlpatterns = [
    #Authentication
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),

    #User Descriptions
    path('general-info/', general_info_list_view, name='general_info_list'),
    path('general-info/<int:pk>/', general_info_detail_view, name='general_info_detail'),

    path('user/<int:user_id>/preference/', user_preference_view, name='user_preference'),
    path('agent/<int:agent_id>/details/', agent_details_view, name='agent_details'),

    # Search, Filtering and Recommendations
    path('properties/search', property_search_view, name='property_search'),
    path('properties/<int:property_id>/recommendation/', property_recommendation_view, name='property_recommendation'),

    #Properties
    path('properties/', property_list_view, name='property-list'),
    path('properties/<int:pk>/', property_detail_view, name='property_detail'),
    path('properties/<int:property_id>/price/', property_price_view, name='property-price'),
    path('properties/<int:property_id>/visuals/', property_visuals_view, name='property_visuals'),
    path('properties/<int:property_id>/review/', property_review_view, name='property_review'),
        path('properties/<int:property_id>/payment_method/', property_payment_method_view, name='property_payment_method'),

    #Property Requests
    path('properties/<int:property_id>/request/', property_request_view, name='property_request'),
    path('properties/<int:property_id>/request/agent', property_request_agent_view, name='property_request_agent'),

    #For Rent
    path('rent/notification/payment/<int:user_id>/', rent_notification_view, name='rent_notification'),
    path('rent/record/<int:user_id>/<int:property_id>/', rent_record_view, name='rent_record'),

    #News
    path('alert/new_deal/<int:property_id>/', alert_new_deal_view, name='alert_new_deal'),
    path('alert/<int:property_id>/request_approval/', alert_property_request_approval_view, name='alert_property_request_approval'),

    #Miscellaneous
    path('property/compare/<int:property_id_1>/<int:property_id_2>/', property_comparison_view, name='property_comparison'),
]