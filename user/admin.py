from django.contrib import admin
from .models import Responsable, Clinicien, Patient, Population, variableEtude, Dossier, Agenda, Parcours, enAttente, Message, Resultat
# Register your models here.


class ResponsableAdmin(admin.ModelAdmin):
    list_display   = ('username')
    list_filter    = ('hopital')
    date_hierarchy = 'user.date_joined'
    ordering       = ('user.date_joined', )
    search_fields  = ('hopital')

class ClinicienAdmin(admin.ModelAdmin):
    list_display   = ('username')
    list_filter    = ('hopital', 'Responsable')
    date_hierarchy = 'user.date_joined'
    ordering       = ('user.date_joined', )
    search_fields  = ('hopital', 'Responsable')

admin.site.register(Responsable)#,ResponsableAdmin )
admin.site.register(Clinicien)#,ClinicienAdmin )
admin.site.register(Patient)
admin.site.register(Population)
admin.site.register(variableEtude)
admin.site.register(Dossier)
admin.site.register(Agenda)
admin.site.register(Parcours)
admin.site.register(enAttente)
admin.site.register(Message)
admin.site.register(Resultat)