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
)

@api_view(["GET", "POST"])
def user_list_create(request):
    if request.method == "GET":
        users = get_user_list()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = create_user(**serializer.validated_data)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def user_detail_update

