from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class PatientRegisterFrom(UserCreationForm):
    email = forms.EmailField(label='Votre email', required=True)
    univ = forms.CharField(max_length=150, label='Votre université :')

    class Meta:
        model = User
        fields = ['username', 'email', 'univ','password1', 'password2']


