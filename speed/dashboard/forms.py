from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import Person


class MyAuthenticationForm(AuthenticationForm):
	username = forms.CharField(label="", widget=TextInput(attrs={'autofocus': "true", 'class': "login well well-sm", 'placeholder': "username"}))
	password = forms.CharField(label="", widget=PasswordInput(attrs={'class': "login well well-sm", 'placeholder': "password"}))

class MyUserCreationForm(UserCreationForm):
	username = forms.CharField(label="", widget=TextInput(attrs={'class': "login well well-sm",'placeholder': "username"}))	
	password1 = forms.CharField(label="", widget=PasswordInput(attrs={'class': "login well well-sm", 'placeholder':"password"}))
	password2 = forms.CharField(label="", widget=PasswordInput(attrs={'class': "login well well-sm", 'placeholder':"re-enter password"}))
	parent = forms.CharField(label="", required=False)
	phone = forms.CharField(label="", widget=TextInput(attrs={'class':"login well well-sm", 'placeholder': "phone number"}))