from django.urls import path
from user.view import view_patient, view_clinicien, view_gestion
from django.contrib.auth import views as auth_views

urlpatterns = [
    ## Connexion et déconnexion
    path('login/', auth_views.LoginView.as_view(template_name='user/ConnectDisconnect/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/ConnectDisconnect/logout.html'), name='logout'),

    ## Partie Patient
    path('patient/', view_patient.register, name='patient'),
    path('profil', view_patient.patient, name="profil"),

    ## Partie Clinicien
    path('registerClinicien/', view_clinicien.registerClinicien, name='registerClinicien'),
    path('clinicien', view_clinicien.clinicien, name="clinicien"),
    path('detail/<str:patient>', view_clinicien.detail, name="detail"),
    #path('detail/datasetDossier/<str:patient>/<int:variable>', view_clinicien.sendDataDossier.as_view),

    ## Partie Gestion
    path('Gestion', view_gestion.Gestion, name='gestion'),
    path('GetPatientClinicien/<int:pkCli>', view_gestion.EnvoieClinicienPatient.as_view()),
    path('EnvoiePopulationPatient/<int:pkPop>', view_gestion.EnvoiePopulationPatient.as_view()),
]
