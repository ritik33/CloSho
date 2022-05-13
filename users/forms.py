from django import forms
from django.forms import fields, widgets
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label='', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(required=True, label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = User


class SignupForm(UserCreationForm):
    password1 = forms.CharField(required=True, label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')
        labels = {'email': '', 'username': ''}
        widgets = {'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                   'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})}


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number',
                  'first_name', 'last_name', 'sex', 'avatar')
        labels = {'username': '', 'email': '', 'phone_number': '',
                  'first_name': '', 'last_name': '', 'sex': '', 'avatar': ''}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                   'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                   'sex': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sex'}),
                   'avatar': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Avatar'})
                   }


class UpdatePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(required=True, label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    new_password2 = forms.CharField(required=True, label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
        labels = {'old_password': '', 'new_password1': '', 'new_password2': ''}
