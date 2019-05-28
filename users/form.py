from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Patient, Clinicien


class PatientRegisterForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model=Patient
        fields= UserCreationForm.Meta.fields + ('custom_field',) 
