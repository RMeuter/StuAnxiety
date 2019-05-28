from django.shortcuts import render
from .form import SectionForm

# Create your views here.

def CreationModule(request):
    form = SectionForm()
    if request.method =='POST':
        pass
    return render(request, "module/MakeModule.html", {'form':form})
