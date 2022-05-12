from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
import uuid
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, max_length=10, primary_key=True)
    username = models.CharField(max_length=50, unique=True, blank=True)
    email = models.EmailField(max_length=254, unique=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(
        upload_to='avatar', default='avatar/default.png', blank=True, null=True)
    choose_sex = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    sex = models.CharField(max_length=50, choices=choose_sex, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(
        auto_now_add=True, blank=True, null=True, editable=True)
    last_login = models.DateTimeField(
        auto_now=True, blank=True, null=True, editable=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def full_name(self):
        return self.first_name + ' ' + self.last_name
