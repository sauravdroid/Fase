from django import forms
from .models import FaseUser
from django.contrib.auth.models import User

class FaseUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']
        #fields = '__all__'
