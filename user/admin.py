from django.contrib import admin
from .models import Clinicien, Patient, Population, variableEtude, Dossier, Agenda, Parcours, enAttente, Message, Resultat


admin.site.register(Clinicien)
admin.site.register(Patient)
admin.site.register(Population)
admin.site.register(variableEtude)
admin.site.register(Dossier)
admin.site.register(Agenda)
admin.site.register(Parcours)
admin.site.register(enAttente)
admin.site.register(Message)
admin.site.register(Resultat)