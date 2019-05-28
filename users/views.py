from django.shortcuts import render
from .models import Clinicien, Patient
# Create your views here.

def register(request):
    ##Enregistremment patient
    if request.method =='POST':
        form = UserRegisterFrom(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Connecte toi maintenant !')
            return redirect('login')
    else:
        form = UserRegisterFrom()
    return render(request, 'users/register/pt.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def user(request):
    return render(request, "users/user.html", {"profil": user})
