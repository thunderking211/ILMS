from collections import UserDict
from logging import PlaceHolder
from multiprocessing.sharedctypes import Value
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from apps.userprofile.models import Profile


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
        ]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'phone_number',
            'birth_date',
            'profile_image'
        ]


class ContactForm(forms.Form):  
	first_name = forms.CharField(max_length = 50, help_text='required',widget=forms.TextInput(attrs={'placeholder': 'Enter First Name'}))
	last_name = forms.CharField(max_length = 50, help_text='required',widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name'}))
	email_address = forms.EmailField(max_length = 150, help_text='required',widget=forms.TextInput(attrs={'placeholder': 'Enter Email-id'}))
	message = forms.CharField(widget = forms.Textarea(attrs={'placeholder': 'Enter Email-id'}), max_length = 2000, help_text='required')

from apps.userprofile.models import homeloan, carloan, personalloan

class homeloanForm(forms.ModelForm):
    
    class Meta:
        model= homeloan
        fields= ["firstname", "lastname", "email", "phone_number", "income", "gender", "MARITAL_STATUS", "loan_type"]
     
 
class carloanForm(forms.ModelForm):
    
    class Meta:
        model= carloan
        fields= ["firstname", "lastname", "email", "phone_number", "income", "gender", "MARITAL_STATUS", "loan_type"]
     
 
class personalloanForm(forms.ModelForm):
    
    class Meta:
        model= personalloan
        fields= ["firstname", "lastname", "email", "phone_number", "income", "gender", "MARITAL_STATUS", "loan_type"]
     
 