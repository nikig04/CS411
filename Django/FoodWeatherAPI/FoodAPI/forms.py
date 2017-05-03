from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from .models import UserProfile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Required')
    last_name = forms.CharField(max_length=30, required=False, help_text='Required')
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')
    password1 = forms.CharField(label= ("Password"), widget=forms.PasswordInput, help_text = ("Must contain at least 8 characters."))
    
    vegetarian = forms.BooleanField(required=False)
    vegan = forms.BooleanField(required=False)
    gluten_free = forms.BooleanField(required=False)
    dairy_free = forms.BooleanField(required=False)
    # whole30 = forms.BooleanField(required=False)
    # ketogenic = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', \
        	'vegetarian', 'vegan','gluten_free', 'dairy_free',)

# class ProfileForm(forms.ModelForm):

#     class Meta:
#        	model = Profile
#         fields = ('username', 'vegatarian', 'vegan')
