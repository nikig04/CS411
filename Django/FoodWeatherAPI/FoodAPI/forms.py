from django import forms
from django.core.exceptions import ValidationError
# from contacts.models import Contact
from .models import User
 
class UserForm(forms.Form):
    # to take the input of username
    username = forms.CharField(max_length=100)
    # to take the input of email
    email = forms.CharField(max_length=100)
    # to take the input of password
    password = forms.CharField(widget=forms.PasswordInput)
