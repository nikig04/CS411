from django import forms
 
class UserForm(forms.Form):
    # to take the input of username
    username = forms.CharField(max_length=100)
    # to take the input of email
    email = forms.CharField(max_length=100)
    # to take the input of password
    password = forms.CharField(max_length=100)