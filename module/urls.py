from django.urls import path
from . import views 

urlpatterns = [
    path('Creation', views.CreationModule, name="Creation"),
              ]
