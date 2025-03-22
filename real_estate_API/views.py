from django.db.models import Avg
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import General_Info, Regular_User, Agent_User, Property_Description, Images, Feedback, Property_Price, PropertyNotification
from .serializers import (GeneralInfoSerializer, RegularUserSerializer, AgentUserSerializer, PropertySerializer,
                          ImagesSerializer, PaymentMethodSerializer, PaymentRecordSerializer, PropertyPriceSerializer,
                          PropertyNotificationSerializer, FeedbackSerializer)
from .service import (
    get_user_list,
    get_user_by_id,
    create_user,
    update_user_by_id,
    delete_user_by_id,
    login_user,
    get_user_preference,
    create_user_preference,
    update_user_preference,
    delete_user_preference,
    get_agent_details,
    create_agent_details,
    update_agent_details,
    delete_agent_details,
    get_property_by_id,
    create_property,
    update_property_by_id,
    delete_property_by_id,
    get_property_visuals,
    get_property_price,
    calculate_average_rating,
    create_property_request,
    assign_agent_to_request,
    get_payment_methods,
    add_payment_method,
    search_properties,
    recommend_properties,
    get_upcoming_payments,
    get_payment_records,
    calculate_payments_left,
    compare_properties_with_payment,
    notify_new_deal,
    notify_property_request_approval
)


@api_view(['POST'])
def register_view(request):
    serializer = GeneralInfoSerializer(data=request.data)
    if serializer.is_valid():
        try:
            general_info = create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                email_address=serializer.validated_data['email_address'],
                location=serializer.validated_data['location'],
                is_agent=serializer.validated_data['is_agent']
            )
            response_data = serializer.data
            response_data['id'] = general_info.id  # Include userID in the response
            return Response(response_data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'detail': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            return Response({'detail': 'Login successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User account is disabled.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def general_info_list_view(request):
    general_info_list = get_user_list()
    serializer = GeneralInfoSerializer(general_info_list, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def general_info_detail_view(request: object, pk: object) -> object:
    if request.method == 'GET':
        general_info = get_user_by_id(pk)
        if general_info:
            serializer = GeneralInfoSerializer(general_info)
            return Response(serializer.data)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PUT':
        general_info = get_user_by_id(pk)
        if general_info:
            serializer = GeneralInfoSerializer(general_info, data=request.data, partial=True)
            if serializer.is_valid():
                update_user_by_id(pk, serializer.validated_data)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        general_info = delete_user_by_id(pk)
        if general_info:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_preference_view(request, user_id):
    if request.method == 'GET':
        user_preference = get_user_preference(user_id)
        if user_preference:
            serializer = RegularUserSerializer(user_preference)
            return Response(serializer.data)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        serializer = RegularUserSerializer(data=request.data)
        if serializer.is_valid():
            user_preference = create_user_preference(user_id, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        user_preference = get_user_preference(user_id)
        if user_preference:
            serializer = RegularUserSerializer(user_preference, data=request.data, partial=True)
            if serializer.is_valid():
                update_user_preference(user_id, serializer.validated_data)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        user_preference = delete_user_preference(user_id)
        if user_preference:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def agent_details_view(request, agent_id):
    if request.method == 'GET':
        agent_details = get_agent_details(agent_id)
        if agent_details:
            serializer = AgentUserSerializer(agent_details)
            return Response(serializer.data)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        serializer = AgentUserSerializer(data=request.data)
        if serializer.is_valid():
            agent_details = create_agent_details(agent_id, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        agent_details = get_agent_details(agent_id)
        if agent_details:
            serializer = AgentUserSerializer(agent_details, data=request.data, partial=True)
            if serializer.is_valid():
                update_agent_details(agent_id, serializer.validated_data)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        agent_details = delete_agent_details(agent_id)
        if agent_details:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def property_list_view(request):
    if request.method == 'GET':
        # Handle GET request: List all properties
        properties = Property_Description.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Handle POST request: Create a new property
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the new property to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PATCH'])
def property_detail_view(request, pk):
    try:
        property_description = Property_Description.objects.get(pk=pk)
    except Property_Description.DoesNotExist:
        return Response({'detail': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PropertySerializer(property_description)
        average_rating = Feedback.objects.filter(property_description=property_description).aggregate(Avg('rating'))[
            'rating__avg']
        if average_rating is None:
            average_rating = 0
        response_data = serializer.data
        response_data['average_rating'] = round(average_rating, 2)

        return Response(response_data)

    # Handle DELETE request: Delete the property
    elif request.method == 'DELETE':
        property_description.delete()
        return Response({'detail': 'Property deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    # Handle PATCH request: Update specific fields of the property
    elif request.method == 'PATCH':
        serializer = PropertySerializer(property_description, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def property_price_view(request, property_id):
    if request.method == 'GET':
        property_description = Property_Description.objects.get(pk=property_id)
        price = property_description.prices.last()
        if price:
            return Response({
                'current_rent_price': price.price_rent,
                'current_full_price': price.price_full,
                'upcoming_rent_price': price.price_rent_next,
                'upcoming_full_price': price.price_full_next
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'No price information available.'}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        property_description = Property_Description.objects.get(pk=property_id)
        serializer = PropertyPriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(property_description=property_description)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def property_visuals_view(request, property_id):
    try:
        # Retrieve the property's images using the related_name
        property_description = Property_Description.objects.get(pk=property_id)
        images = property_description.images.all()

        # Serialize the images
        serializer = ImagesSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Property_Description.DoesNotExist:
        return Response({'detail': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def property_price_view(request, property_id):
    try:
        if request.method == 'GET':
            property_description = Property_Description.objects.get(pk=property_id)
            price = property_description.prices.last()
            if price:
                return Response({
                    'current_rent_price': price.price_rent,
                    'current_full_price': price.price_full,
                    'upcoming_rent_price': price.price_rent_next,
                    'upcoming_full_price': price.price_full_next
                }, status=status.HTTP_200_OK)
            return Response({'detail': 'No price information available.'}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == 'POST':
            property_description = Property_Description.objects.get(pk=property_id)
            serializer = PropertyPriceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(property_description=property_description)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Property_Description.DoesNotExist:
        return Response({'detail': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def property_review_view(request, property_id):
    if request.method == 'GET':
        average_rating = calculate_average_rating(property_id)
        if average_rating is not None:
            return Response({
                'property_id': property_id,
                'average_rating': average_rating,
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(property_description_id=property_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def property_request_view(request, property_id):
    try:
        user_id = request.data.get('user_id')
        new_request = create_property_request(user_id=user_id, property_id=property_id)
        return Response({
            'detail': 'Request submitted successfully.',
            'request_id': new_request.id,
            'status': new_request.status,
            'request_date': new_request.request_date,
        }, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist as e:
        return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def property_request_agent_view(request, property_id):
    try:
        user_id = request.data.get('user_id')
        agent_id = request.data.get('agent_id')
        updated_request = assign_agent_to_request(user_id=user_id, property_id=property_id, agent_id=agent_id)
        return Response({
            'detail': 'Agent assigned successfully.',
            'request_id': updated_request.id,
            'agent_id': updated_request.agent.id,
            'status': updated_request.status,
        }, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist as e:
        return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def property_payment_method_view(request, property_id):
    if request.method == 'GET':
        try:
            payment_methods = get_payment_methods(property_id)
            if payment_methods:
                serializer = PaymentMethodSerializer(payment_methods)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'detail': 'No payment methods available.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        try:
            rent_price = request.data.get('rent_price')
            full_price = request.data.get('full_price')
            rent_duration_months = request.data.get('rent_duration_months')

            # Add a new payment method
            payment = add_payment_method(property_id, rent_price, full_price, rent_duration_months)
            serializer = PaymentMethodSerializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def property_search_view(request):
    description = request.query_params.get('description')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')

    properties = search_properties(description, min_price, max_price)
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def property_recommendation_view(request, user_id):
    try:
        recommended_properties = recommend_properties(user_id)

        serializer = PropertySerializer(recommended_properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def rent_notification_view(request, user_id):
    upcoming_payments = get_upcoming_payments(user_id)
    if upcoming_payments.exists():
        serializer = PaymentRecordSerializer(upcoming_payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'detail': 'No upcoming payments.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def rent_record_view(request, user_id, property_id):
    payment_records = get_payment_records(user_id)
    payments_left = calculate_payments_left(user_id, property_id)

    # Serialize payment records
    serializer = PaymentRecordSerializer(payment_records, many=True)
    response_data = {
        'payments_left': payments_left,
        'payment_records': serializer.data
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def property_comparison_view(request, property_id_1, property_id_2):
    try:
        comparison_data = compare_properties_with_payment(property_id_1, property_id_2)
        return Response(comparison_data, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def alert_new_deal_view(request, property_id):
    try:
        notifications = notify_new_deal(property_id)
        return Response(
            {'detail': f"New deal notifications sent to {len(notifications)} users."},
            status=status.HTTP_201_CREATED
        )
    except ValueError as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def alert_property_request_approval_view(request, property_id):
    try:
        notification = notify_property_request_approval(property_id)
        return Response(
            {'detail': f"Notification sent to {notification.user.username}."},
            status=status.HTTP_201_CREATED
        )
    except ValueError as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_notifications_view(request, user_id):
    notifications = PropertyNotification.objects.filter(user__id=user_id, is_read=False).order_by('-created_at')
    serializer = PropertyNotificationSerializer(notifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)