from django.shortcuts import render, redirect
from .models import Clinicien, Patient
from .form import PatientRegisterForm
from django.contrib import messages
# Create your views here.
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def register(request):
    ##Enregistremment patient
    if request.method =='POST':
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('prenom')
            messages.success(request, f'Account created for {username}! Connecte toi maintenant !')
            return redirect('login')
    else:
        form = PatientRegisterForm()
    return render(request, 'users/register/pt.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def user(request):
    return render(request, "users/user.html", {"profil": user})
#