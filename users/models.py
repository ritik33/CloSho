from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
import uuid


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, max_length=10,
                          primary_key=True, unique=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    dob = models.DateField(verbose_name='DOB',
                           auto_now=False, auto_now_add=False, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatar', blank=True, null=True)
    choose_sex = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )
    sex = models.CharField(max_length=50, choices=choose_sex, blank=True)
    phone_number = models.PositiveIntegerField(blank=True, null=True)
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
