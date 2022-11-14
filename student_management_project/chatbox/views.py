from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import render
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from .serializers import *

# Create your views here.
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            # "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        _, token = AuthToken.objects.create(user)
        return Response({
            # "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, ])
def update_user(request):

    user = request.user
    user_serializer = UserSerializer(user, data=request.data, partial=True)
    if user_serializer.is_valid():
        user_serializer.save()
        return Response(user_serializer.data)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def delete_user(request):

    # Get User Id Based On User Token
    user_id = request.user.id
    try:
        # Delete From Table
        student_to_delete = CustomUser.objects.get(
            id=user_id)
        student_to_delete.delete()
        return Response({'student_delete': 'success'})
    except CustomUser.DoesNotExist:
        return Response({'student_delete': 'does_not_exist'})


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def get_user(request):
    user_id = request.user.id
    print(user_id)
    try:
        id = request.data['id']
        queryset = CustomUser.objects.get(id = user_id)
        serializer = UserSerializer(queryset)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({'student_delete': 'does_not_exist'})
