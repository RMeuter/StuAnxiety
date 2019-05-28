from django.shortcuts import render
from .form import SectionForm
# Utilisation d'ajax
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.views.generic import View
from .models import Section

# Create your views here.
# https://www.techiediaries.com/python-django-ajax/


class SectionList (View):
    def get(self, request):
        module = list(Section.objects.all().values())
        data = dict()
        data['module'] = module
        return JsonResponse(data)



class  RoomDetail(View):
    def  get(self, request, pk):
        section = get_object_or_404(Section, pk=pk)
        data =  dict()
        data['section'] = model_to_dict(section)
        return JsonResponse(data)





#------------------------------------------------

def CreationModule(request):
    form = SectionForm()
    return render(request, "module/MakeModule.html", {'form':form})



"""
from django import forms
from .models import Room




from django.urls import path, include
from django.views.generic.base import TemplateView
from rooms import views

urlpatterns = [
    path('rooms/', TemplateView.as_view(template_name="rooms/main.html"), name='room_main'),
    path('rooms/list', views.RoomList.as_view(), name='room_list'),
    path('rooms/create', views.RoomCreate.as_view(), name='room_create'),
    path('rooms/update/<int:pk>', views.RoomUpdate.as_view(), name='room_update'),
    path('rooms/delete/<int:pk>', views.RoomDelete.as_view(), name='room_delete'),
    path('rooms/<int:pk>', views.RoomDetail.as_view(), name='room_detail'), 
]
"""