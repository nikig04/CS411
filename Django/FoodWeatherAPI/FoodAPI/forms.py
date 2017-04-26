from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Required')
    last_name = forms.CharField(max_length=30, required=False, help_text='Required')
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')
    password1 = forms.CharField(label= ("Password"), widget=forms.PasswordInput, help_text = ("Must contain at least 8 characters."))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

# class UserForm(forms.Form):
#     # to take the input of username
#     username = forms.CharField(max_length=100)
#     # to take the input of email
#     email = forms.CharField(max_length=100)
#     # to take the input of password
#     password = forms.CharField(widget=forms.PasswordInput)
