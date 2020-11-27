from django.contrib.auth.models import BaseUserManager
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User
        required_fields = ('username', 'email')

    def create(self, validated_data):
        abc = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
        user = super(UserSerializer, self).create(validated_data)
        user.email = self.validated_data['email']
        password = BaseUserManager().make_random_password(length=5,
                                                          allowed_chars=abc)
        user.password = BaseUserManager(). \
            make_random_password(length=5, allowed_chars=abc)
        user.set_password(password)
        if user.role == 'moderator':
            user.is_staff = True
        elif user.role == 'admin':
            user.is_admin = True
        user.save()
        return user


class CreateAuthKeySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('email',)
        model = User


class CheckAuthKeySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    auth_code = serializers.CharField(required=True)

    class Meta:
        fields = ('email', 'auth_code')
        model = User
