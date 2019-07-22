from django.contrib import admin
from .models import Module, Section, Question, Reponse, Sequence, Ordre

# Register your models here.
"""
"""
admin.site.register(Reponse)
admin.site.register(Question)
admin.site.register(Module)
admin.site.register(Section)
admin.site.register(Sequence)
admin.site.register(Ordre)

