from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import General_Info
from .serializers import UserSerializer
from .service import (
    get_user_list,
    get_user_by_id,
    create_user,
    update_user_by_id,
    delete_user_by_id,
    login_user
)


@api_view(['POST'])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        general_info = create_user(
            username=serializer.validated_data['username'],
            email_address=serializer.validated_data['email_address'],
            location=serializer.validated_data['location'],
            is_agent=serializer.validated_data['is_agent']
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            general_info = create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                email_address=serializer.validated_data['email_address'],
                location=serializer.validated_data['location'],
                is_agent=serializer.validated_data['is_agent']
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
    serializer = UserSerializer(general_info_list, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def general_info_detail_view(request, pk):
    if request.method == 'GET':
        general_info = get_user_by_id(pk)
        if general_info:
            serializer = UserSerializer(general_info)
            return Response(serializer.data)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PUT':
        general_info = get_user_by_id(pk)
        if general_info:
            serializer = UserSerializer(general_info, data=request.data, partial=True)
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


