from django.shortcuts import render, redirect

from .form import PatientRegisterFrom
from .models import Patient, Clinicien
#from django.http import Http404

# Create your views here.
def register(request):
    ##Enregistremment patient
    if request.method =='POST':
        form = PatientRegisterFrom(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
    else:
        form = PatientRegisterFrom()
    return render(request, 'user/register/pt.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def patient(request):
    return render(request, "user/patient.html", {"profil": patient})

@login_required
def clinicien(request):
    return render(request, "user/Clinicien.html", {"profil": Clinicien})
