from django import forms
from django.contrib.auth.models import User
from .models import Customer
from .models import Room, Booking
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'is_available', 'price_per_night']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer', 'room', 'check_in', 'check_out']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'is_customer', 'is_staffuser']
