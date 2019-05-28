from django.forms import ModelForm
from .models import Module, Section

class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ['nom']

class SectionForm (ModelForm):
    class Meta:
        model=Section
        fields=['ordre', 'text', 'image']
