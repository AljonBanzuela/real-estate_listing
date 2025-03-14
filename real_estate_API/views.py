from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import General_Info, Regular_User, Agent_User
from .serializers import GeneralInfoSerializer, RegularUserSerializer, AgentUserSerializer
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
    delete_agent_details
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
    email_address = request.data.get('email_address')
    password = request.data.get('password')
    tokens = login_user(email_address, password)
    if tokens:
        return Response(tokens, status=status.HTTP_200_OK)
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def general_info_list_view(request):
    general_info_list = get_user_list()
    serializer = GeneralInfoSerializer(general_info_list, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def general_info_detail_view(request, pk):
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


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
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
