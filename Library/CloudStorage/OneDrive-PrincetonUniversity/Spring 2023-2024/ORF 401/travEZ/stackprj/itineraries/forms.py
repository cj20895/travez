from django import forms
from django.contrib.auth.models import User
from .models import Itinerary

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ['name', 'description', 'image']
        
