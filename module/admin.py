from django.contrib import admin
from .models import Module, Section, Questionnaire, Question, Reponse, Sequence, Ordre

# Register your models here.
"""
"""
admin.site.register(Reponse)
admin.site.register(Question)
admin.site.register(Questionnaire)
admin.site.register(Module)
admin.site.register(Section)
admin.site.register(Sequence)
admin.site.register(Ordre)

class ModuleAdmin(admin.ModelAdmin):
    list_display   = ('nom', 'updated_at', 'created_at', )
    list_filter    = ('auteur','categorie',)
    date_hierarchy = 'created_at'
    ordering       = ('created_at', )
    search_fields  = ('nom')