########################################### Gestionnnaire
# Partie ajax
from django.http import JsonResponse
from django.views.generic import View
# Partie view
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
# Model et form propre au site
from user.form import GroupCreationForm, PatientPopulationForm, PatientClinicienForm, GroupForm
from user.models import Patient, Clinicien, Population, Group
# Requete et aggregat
from django.db.models import Count
import random


@login_required
@permission_required("user.Clinicien_Responsable")
def Gestion(request):
    allClinicien = Clinicien.objects.all().values('pk', "user__last_name", "user__first_name")
    allGroupe = Population.objects.filter(categorie__gt=1)

    ### Reception :
    if request.method== "POST":
        if "Clinicien" in request.POST and "clinicien_du_patient" in request.POST :
            clinicien = Clinicien.objects.get(pk=request.POST.get("Clinicien"))
            listPat = request.POST.getlist("clinicien_du_patient")
            for var in listPat:
                pat = Patient.objects.get(pk=var)
                pat.clinicienACharge=clinicien
                pat.save()
        elif "Population" in request.POST and "patient" in request.POST:

            pop = Population.objects.get(pk=request.POST.get("Population"))
            listPat = request.POST.getlist("patient")
            print("rentre ! ", pop," : ", listPat)
            for var in listPat:
                pat = Patient.objects.get(pk=var)
                pat.groupePatients=pop
                pat.save()
        if GroupCreationForm(request.POST).is_valid() and GroupForm(request.POST).is_valid():
            formG = GroupForm(request.POST)
            formP = GroupCreationForm(request.POST)
            insPopulation = formP.save(commit=False)
            insGroupe = formG.save()
            insPopulation.groupe = insGroupe
            insPopulation.save()
        else:
            formP = GroupCreationForm()
            formG = GroupForm()
    else:
        formP = GroupCreationForm()
        formG = GroupForm()
    return render(request, "user/clinicien/gestionResponsable.html", {"PopulationFrom": formP,"GroupeForm":formG, "allClinicien":allClinicien, "allGroupe":allGroupe})

class EnvoiePopulationPatient(View):
    def get(self, request, pkPop):
        listPatient=Patient.objects.filter(groupePatients=pkPop).values("user__first_name", "user__last_name")
        gestionList=dict()
        gestionList["listPatient"]=list(listPatient)
        gestionList["noListPatient"]="{0}".format(PatientPopulationForm(population=pkPop))
        return JsonResponse(gestionList)

class EnvoieClinicienPatient(View):
    def get(self, request, pkCli):
        listPatient=Patient.objects.filter(clinicienACharge__pk=pkCli).values("user__first_name", "user__last_name")
        gestionList=dict()
        gestionList["listPatient"]=list(listPatient)
        gestionList["noListPatient"]="{0}".format(PatientClinicienForm(clinicien=pkCli))
        return JsonResponse(gestionList)