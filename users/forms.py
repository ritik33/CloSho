from django import forms
from django.forms import fields, widgets
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label='', widget=forms.EmailInput(
        attrs={'class':'form-control','placeholder': 'Email'}))
    password = forms.CharField(required=True, label='', widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder': 'Password'}))

    class Meta:
        model = User


class SignupForm(UserCreationForm):
    password1 = forms.CharField(required=True, label='', widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder': 'Password'}))
    password2 = forms.CharField(required=True, label='', widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')
        labels = {'email': '', 'username': ''}
        widgets = {'email': forms.EmailInput(attrs={'class':'form-control','placeholder': 'Email'}),
                   'username': forms.TextInput(attrs={'class':'form-control','placeholder': 'Username'})}
