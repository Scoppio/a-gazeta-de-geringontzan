from django import forms
from .models import apikeys

class ApiForm(forms.ModelForm):
    class Meta:
        model = apikeys
        exclude = ('id', 'validToken')
