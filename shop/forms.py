from django import forms
from django.forms import fields, widgets
from .models import ShippingAddress, OrderItem


class ShippingAddressForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = ('name', 'phone_number', 'address',
                  'zipcode', 'city', 'state', 'country',)
        labels = {'name': '', 'phone_number': '', 'address': '',
                  'zipcode': '', 'city': '', 'state': '', 'country': ''}
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
                   'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
                   'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
                   'zipcode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}),
                   'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
                   'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
                   'country': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Country'}),
                   }


class QuantityForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('quantity',)
        labels = {'quantity': ''}
        widgets = {'quantity': forms.NumberInput(
            attrs={'class': 'form-control', 'min': 1})}
