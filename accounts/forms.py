from django import forms
from .models import Client




class PreSetAuthorizedUserForm(forms.Form):
    first_name = forms.CharField(max_length=70)
    last_name = forms.CharField(max_length=70)
    email = forms.EmailField(max_length=255)
    code = forms.CharField(max_length=15)


class SetNewUserPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=30)
    password2 = forms.CharField(max_length=30)


class CreateClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['trainer', 'first_name', 'last_name']


class SetPinForm(forms.Form):
    pin1 = forms.CharField(max_length=4)
    pin2 = forms.CharField(max_length=4)
    agree_to_use_as_signature = forms.BooleanField()