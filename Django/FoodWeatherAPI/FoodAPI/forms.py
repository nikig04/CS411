from django import forms
from django.core.exceptions import ValidationError
from contacts.models import Contact
 
class UserForm(forms.Form):
    # to take the input of username
    username = forms.CharField(max_length=100)
    # to take the input of email
    email = forms.CharField(max_length=100)
    # to take the input of password
    password = forms.CharField(max_length=100)

# class ContactForm(forms.ModelForm):
#     confirm_email = forms.EmailField(
#         label="Confirm email",
#         required=True,
#     )

#     class Meta:
#         model = Contact

#     def __init__(self, *args, **kwargs):

#         if kwargs.get('instance'):
#             email = kwargs['instance'].email
#             kwargs.setdefault('initial', {})['confirm_email'] = email

#         return super(ContactForm, self).__init__(*args, **kwargs)