from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('***')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None):
        user = self.create_user(email=self.normalize_email(email),
                                password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.role = 'admin'
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    roles = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    )

    email = models.EmailField(verbose_name='email', max_length=30, unique=True,
                              blank=False)
    username = models.CharField(max_length=20)
    date_joinded = models.DateTimeField(verbose_name='date joined',
                                        auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    bio = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=9, choices=roles, default='user')
    auth_code = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=10, blank=True)
    last_name = models.CharField(max_length=15, blank=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
