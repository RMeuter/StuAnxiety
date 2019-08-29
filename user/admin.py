from django.contrib import admin
from .models import Clinicien, Patient, Population, variableEtude, Dossier, Agenda, Parcours, enAttente, Message, Resultat

class ClinicienAdmin (admin.ModelAdmin):
    list_display = ["user", "equipe"]
    list_filter = ["equipe"]
    ordering = ("user", "equipe")
    search_fields = ["user"]

class PatientAdmin (admin.ModelAdmin):
    list_display = ("user", "groupePatients", "clinicienACharge", "sequence", "dateFinTherapie")
    list_filter = ("groupePatients", "clinicienACharge", "dateFinTherapie")
    ordering = ("groupePatients", "clinicienACharge","-dateFinTherapie")
    search_fields = ("groupePatients", "clinicienACharge", "dateFinTherapie")

class PopulationAdmin (admin.ModelAdmin):
    list_display = ["groupe", "categorie"]
    list_filter = ["categorie", "lieu"]
    ordering = ["categorie"]
    search_fields = ["groupe", "categorie", "sequence"]

class variableEtudeAdmin(admin.ModelAdmin):
    list_display = ["nom","typeStatistique","seuilMoyen", "seuilMaximal", "seuilMinimal"]
    list_filter = ["typeStatistique"]
    ordering = ["typeStatistique","nom"]

class DossierAdmin(admin.ModelAdmin):
    list_display = ["variable", "resultat", "patient"]
    list_filter = ["variable", "patient", "enAttente__dateFin"]
    ordering = ["patient", "variable", "enAttente__dateFin"]
    date_hierarchy = "enAttente__dateFin"
    search_fields = ["patient", "variable"]


admin.site.register(Clinicien, ClinicienAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Population, PopulationAdmin)
admin.site.register(variableEtude, variableEtudeAdmin)
admin.site.register(Dossier, DossierAdmin)
admin.site.register(Agenda)
admin.site.register(Parcours)
admin.site.register(enAttente)
admin.site.register(Message)
admin.site.register(Resultat)