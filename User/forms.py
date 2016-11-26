from django import forms
from django.contrib.auth.models import User
from .models import CreatedApps


class FaseUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        # fields = '__all__'


class CreateAppForm(forms.ModelForm):
    class Meta:
        model = CreatedApps
        exclude = ['app_encrypted_key', 'created_at']


class CheckAppForm(forms.Form):
    secret_key = forms.CharField(max_length=100)
    encrypted_key = forms.CharField(max_length=100)
