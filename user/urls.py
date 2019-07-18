from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profil', views.patient, name="profil"),
    path('clinicien', views.clinicien, name="clinicien"),
    path('detail/<int:patient>', views.detail, name="detail"),
    path('register/', views.register, name='register'),
    path('registerClinicien/', views.registerClinicien, name='registerClinicien'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),

   path('Gestion', views.Gestion, name='gestion'),
    path('GetPatientClinicien/<int:pkCli>', views.GestionClinicien.as_view()),
    path('GetPatientGroupe/<int:pkPop>', views.GestionGroupe.as_view()),
]
