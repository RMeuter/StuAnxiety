# Partie view
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
# Model et form propre au site
from user.models import Patient, Clinicien, User, Population, enAttente, Agenda, Group
from user.form import UserRegisterFrom, PatientRegisterFrom
# Requete et aggregat
from django.db.models import F, IntegerField, ExpressionWrapper, Count
# Time
from django.utils import timezone

@login_required
@permission_required("user.parcours_Patient_Suivie")
def patient(request):
    '''
    Il faut faire la requete de enAttente pour les pourcentage
    Gérer les messages par fonction ajax !
    Faire le questionnaire sur une autre page.
    Liste de requete :
    - Enattente -> module 
    - Messagerie -> message -> Ajax
    - Notification -> agenda  -> Ajax
    '''
    patient = request.user.patient
    ####### Barre de progression 
    ModuleenAttente = enAttente.objects.filter(patient=patient, dateVisible__lte=timezone.now()).values('ordreAtteint', 'module__nom', 'module__nbSection','module__isQuestionnaireOnly', 'module__pk')
    if not ModuleenAttente.exists():
        ModuleenAttente=None
    else: 
        ModuleenAttente = ModuleenAttente.annotate(progress=ExpressionWrapper((100*F('ordreAtteint'))/F('module__nbSection'),output_field=IntegerField()))
        print(ModuleenAttente)
    ####### Interation message agenda
    rdv = Agenda.objects.filter(patient=patient, clinicien=patient.clinicienACharge).values("objet","debut","duree")
    return render(request, "user/patient/patient.html", {
        "progressModule": ModuleenAttente,
        "rendezvous":rdv,
        "salon":patient.pk,
    })

########################################### Inscription

# Create your views here.
def register(request):
    ##Enregistremment patient
    if request.method =='POST':
        formU = UserRegisterFrom(request.POST)
        formP = PatientRegisterFrom(request.POST)
        if formU.is_valid() and formP.is_valid() :
            use = formU.save()
            pat = Patient.objects.create(user=use)
            """
            ici il faut trouver un clinicien
            user et patient! -> voir optimisation
            """
            if Population.objects.filter(categorie=4).exists():
            # Affecte un groupe categorie 4 de patient avec le moins de patient
                pop = Population.objects.filter(categorie=4).annotate(minPat=Count('patient')).order_by('minPat').first()
            else:
                #Creation d'un group et d'une population 
                group = Group.objects.create(name="Groupe catégorie 4 encore non-nommé numéro : {0}".format(Population.objects.filter(categorie=4).count()))
                group.save()
                pop = Population.objects.create(categorie=4,groupe=group)
                pop.save()
            pat.groupePatients = pop
            # Affecte un clinicien
            if Clinicien.objects.all().exists():
                # Requete du min(nbPatient), et prise aléatoire
                clinicien = Clinicien.objects.annotate(minPatient=Count('clinicien_du_patient')).order_by('minPatient').first()
            else:
                # Seulement pour les tests en réalité cela ne sera pas comme ça !
                try:
                    usercli = User.objects.get(username="Inconnu")
                except User.DoesNotExist:
                    usercli = User.objects.create(username="Inconnu", last_name="No last name", first_name="No frist name", email="unkownmail@mail.fr", password="noRealyPassPass") 
                    usercli.save()
                clinicien = Clinicien.objects.create(user=usercli)
                clinicien.save()
            pat.clinicienACharge = clinicien
            
            PatientRegisterFrom(request.POST, instance=pat).save()
            return redirect('login')
    else:
        formU = UserRegisterFrom()
        formP = PatientRegisterFrom()
    return render(request, 'user/patient/../templates/user/clinicien/pt.html', {'formU': formU, 'formP': formP})