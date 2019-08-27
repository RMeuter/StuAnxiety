from django.contrib import admin
from .models import Module, Section, Question, Reponse, Sequence, Ordre

# Register your models here.
"""
"""
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'isVisible', 'isQuestionnaireOnly', 'questionnaireDependant')
    list_filter = ('isQuestionnaireOnly','isVisible')
    ordering = ("isQuestionnaireOnly", "isVisible")
    search_fields = ("nom", 'isVisible', 'isQuestionnaireOnly')

class SectionAdmin(admin.ModelAdmin):
    list_display = ("module", 'titre', 'ordre', 'SectionType')
    list_filter =('module', "SectionType")
    ordering = ('module', 'ordre')
    search_fields = ('module', 'titre', 'ordre')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question", "inputType")
    list_filter = ("isMultipleRep","inputType")
    search_fields = ("question", "inputType")

class ReponseAdmin(admin.ModelAdmin):
    list_display = ("reponse","question")
    list_filter = ("question", "reponse")
    ordering = ("question","reponse")
    search_fields = ("question", "reponse")

class SequenceAdmin(admin.ModelAdmin):
    list_display = ("nom", "nbModule")

class OrderAdmin(admin.ModelAdmin):
    list_display = ("sequence", "ordre", "module")
    list_filter = ("sequence", "module")
    ordering = ("sequence", "ordre")
    search_fields = ("sequence", "module", "ordre")

admin.site.register(Reponse, ReponseAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Ordre, OrderAdmin)

