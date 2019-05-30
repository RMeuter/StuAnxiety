from django.urls import path
from . import views 
from django.views.generic.base import TemplateView

urlpatterns = [
    path('Creation', views.CreationModule, name="Creation"),
    path('', TemplateView.as_view(template_name="module/Module.html"), name='module'),
    path('sections/list', views.SectionList.as_view(), name='section_list'),
    path('sections/create', views.CreateSection.as_view(), name='section_create'),
    path('sections/update/<int:pk>', views.SectionUpdate.as_view(), name='section_update'),
    path('sections/delete/<int:pk>', views.SectionDelete.as_view(), name='section_delete'),
    path('sections/form', views.EnvoieForm.as_view(), name='section_form'),
              ]
