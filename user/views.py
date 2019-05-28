from django.shortcuts import render, redirect
from django.contrib import messages
from .form import PatientRegisterFrom
from .models import Patient
#from django.http import Http404

# Create your views here.
def register(request):
    ##Enregistremment patient
    if request.method =='POST':
        form = PatientRegisterFrom(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Connecte toi maintenant !')
            return redirect('login')
    else:
        form = PatientRegisterFrom()
    return render(request, 'user/register/pt.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def user(request):
    return render(request, "user/user.html", {"profil": user})
