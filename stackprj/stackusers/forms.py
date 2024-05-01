from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.db.models import fields
from .models import Profile
from .models import Person

class UserRegisterForm(UserCreationForm):
    email = models.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'phone', 'image']


from django import forms
from .models import Person

STATE_CHOICES = [('', 'Origination State')]+ [
    ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), 
    ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), 
    ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), 
    ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), 
    ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), 
    ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), 
    ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), 
    ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), 
    ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), 
    ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), 
    ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), 
    ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), 
    ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
]

DESTINATION_STATE_CHOICES = [('', 'Destination State')] + [
    ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), 
    ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), 
    ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), 
    ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), 
    ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), 
    ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), 
    ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), 
    ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), 
    ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), 
    ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), 
    ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), 
    ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), 
    ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
]




class RideForm(forms.Form):
  search_origin = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Origin City', 'style': 'width: 300px;', 'class': 'form-control'}), label="",max_length=64, required=False)
  # forms.CharField())

  searchstate_origin = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Origin State Abbreviation', 'style': 'width: 300px;', 'class': 'form-control'}),label="",max_length=2, required=False)
  
  search_destination = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Destination City', 'style': 'width: 300px;', 'class': 'form-control'}), label="",max_length=64, required=False)
  # attrs={'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control

  ## NEW
  searchstate = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Destination State Abbreviation', 'style': 'width: 300px;', 'class': 'form-control'}),label="",max_length=2, required=False)


# class NewRideForm(forms.ModelForm):
#   class Meta:
#     model = Person
#     exclude = []
class NewRideForm(forms.ModelForm):
    origination_state = forms.ChoiceField(choices=STATE_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px;'}), required=True)
    destination_state = forms.ChoiceField(choices=DESTINATION_STATE_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px;'}), required=True)

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'origination', 'origination_state', 'destination_city', 'destination_state', 'date', 'time', 'taking_passengers', 'pet_friendly', 'accessible', 'seats_available', 'vehicle_type']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'style': 'width: 300px;', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'style': 'width: 300px;', 'class': 'form-control'}),
            'origination': forms.TextInput(attrs={'placeholder': 'Origin City', 'style': 'width: 300px;', 'class': 'form-control'}),
            'destination_city': forms.TextInput(attrs={'placeholder': 'Destination City', 'style': 'width: 300px;', 'class': 'form-control'}),
            'date': forms.DateInput(attrs={'placeholder': 'Date (YYYY-MM-DD)', 'type': 'date', 'style': 'width: 300px;', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'placeholder': 'Time (HH:MM)', 'type': 'time', 'style': 'width: 300px;', 'class': 'form-control'}),
            'seats_available': forms.NumberInput(attrs={'placeholder': 'Seats Available', 'style': 'width: 300px;', 'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'style': 'width: 300px;', 'class': 'form-control'}),
        }
        labels = {
            'first_name': '',
            'last_name': '',
            'origination': '',
            'origination_state': '',
            'destination_city': '',
            'destination_state': '',
            'date': '',
            'time': '',
            'taking_passengers': 'Taking Passengers',
            'pet_friendly': 'Pet Friendly',
            'accessible': 'Accessible',
            'seats_available': '',
            'vehicle_type': '',
        }


