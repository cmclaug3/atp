from django import forms
from .models import Session
from accounts.models import Client



class DateInput(forms.DateInput):
    input_type = 'date'

class ServeSessionForm(forms.Form):
    # date = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'date'}))
    trainer_pin = forms.CharField(max_length=20, widget=forms.PasswordInput())
    client_pin = forms.CharField(max_length=20, widget=forms.PasswordInput())


class BurnSessionForm(forms.Form):
    # date = forms.DateTimeField()
    trainer_pin = forms.CharField(max_length=20)
    confirmation = forms.BooleanField()


