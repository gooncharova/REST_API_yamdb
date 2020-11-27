from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import BaseUserManager
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import UserSerializer, CreateAuthKeySerializer, \
    CheckAuthKeySerializer


@api_view(['POST'])
def api_auth_key(request):
    serializer = CreateAuthKeySerializer(data=request.data)
    email = request.data['email']
    if serializer.is_valid():
        b = BaseUserManager()
        abc = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
        auth_code = b.make_random_password(length=10, allowed_chars=abc)
        user = User.objects.get(email=email)
        user.auth_code = make_password(auth_code)
        user.save()
        send_mail('Your auth code',
                  f'Your auth code {auth_code}',
                  'yamdb@yamdb.ru',
                  {user.email})
        return Response(f'Code send to {user.email}',
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = CheckAuthKeySerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        auth_code = serializer.data.get('auth_code')
        user = get_object_or_404(User, email=email)
        if check_password(auth_code, user.auth_code):
            token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            return Response({'token': f'{token}',
                             'refresh_token': f'{refresh_token}'},
                            status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Wrong auth code'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]


@api_view(['GET', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def get_current_user(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
