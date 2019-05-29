from django.shortcuts import render
from .form import SectionForm
# Utilisation d'ajax
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.views.generic import View, CreateView
from .models import Section

# Create your views here.
# https://www.techiediaries.com/python-django-ajax/


class SectionList (View):
    def get(self, request):
        module = list(Section.objects.all().values())
        data = dict()
        data['module'] = module
        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class  CreateSection(CreateView):
    def  post(self, request):
        data =  dict()
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save()
            data['section'] = model_to_dict(section)
        else:
            data['error'] =  "form not valid!"
        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class  SectionUpdate(View):
    def  post(self, request, pk):
        data =  dict()
        section = Section.objects.get(pk=pk)
        form = SectionForm(instance=section, data=request.POST)
        if form.is_valid():
            section = form.save()
            data['section'] = model_to_dict(section)
        else:
            data['error'] =  "form not valid!"
        return JsonResponse(data)

class  SectionDelete(View):
    def  post(self, request, pk):
        data =  dict()
        section = Section.objects.get(pk=pk)
        if section:
            section.delete()
            data['message'] =  "Section deleted!"
        else:
            data['message'] =  "Error!"
        return JsonResponse(data)

#class EnvoieForm
#------------------------------------------------

def CreationModule(request):
    form = SectionForm()
    return render(request, "module/MakeModule.html", {'form':form})

