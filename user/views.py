# Partie ajax
from django.http import JsonResponse, HttpResponse
from django.views.generic import View

# Partie user
from django.shortcuts import render, redirect
from .models import Patient, Clinicien, User, Population, enAttente, Agenda, Group, variableEtude, Dossier
from module.models import Question, Reponse,Ordre
#from django.http import Http404

# Mise en forme des données
from module.form import OrdreForm 
from .form import AgendaForm, AjoutQuestForm, PatientClinicienForm, PatientGroupForm


from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import F, IntegerField, ExpressionWrapper

from django.db.models import Sum, Max


@login_required
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
    return render(request, "user/patient.html", {
        "progressModule": ModuleenAttente,
        "rendezvous":rdv,
        "salon":patient.pk,
    })


@login_required
def clinicien(request):
    """
    Requete :
    Liste patient message
    Liste patient groupe et resultat
    """
    # Fonction liée au patient
    listPatients = Patient.objects.filter(clinicienACharge=request.user.clinicien).values('user__first_name','user__last_name','user__last_login','groupePatients__groupe__name', 'pk', 'NoSeeMsgQuantity', 'lastScore')
    print(listPatients)
    nbPatient=listPatients.count()
    nbMesg=listPatients.aggregate(nbmsg=Sum('NoSeeMsgQuantity'))
    # Fonction lié à l'agenda
    # https://docs.djangoproject.com/fr/2.2/ref/models/database-functions/
    listAgenda = Agenda.objects.filter(clinicien=request.user.clinicien).values('patient__user__last_name','patient__user__first_name','debut__time','duree','debut__date', 'objet')
    if not listAgenda.exists():
        listAgenda = None
    if nbPatient == 0:
        print("J'ai pas de patient je suis mauvais pour finir")
        listPatients=None
    return render(request, "user/clinicien/Clinicien.html", {
        "listePatients":listPatients,
        "nbPatient":nbPatient,
        "nbMesgNonLu":nbMesg['nbmsg'],
        "Calendrier":listAgenda
    })


@login_required
def detail(request, patient):
    """
    Voir pour un object404 pour eviter que les cliniciens n'ailles sur les autre dossiers.
    Faire attention entre la différence entre le pk et uuci !
    """

    ############# Patient
    monPatient=Patient.objects.values("user__last_name", "user__first_name", "user__email", "telephone","skype", "sequence", "dateFinTherapie").get(pk=patient)
    print(monPatient)
    ##################### Form agenda
    if request.method == "POST":
        formA = AgendaForm(request.POST,patient=patient,clinicien=request.user.clinicien)
        if formA.is_valid():
            formA.save()
        else:
            formA = AgendaForm(patient=patient,clinicien=request.user.clinicien)
    else:
        formA = AgendaForm(patient=patient,clinicien=request.user.clinicien)

    ##################### Form questionnaire
    if request.method == "POST":
        formAffectQuest = AjoutQuestForm(request.POST,patient=patient)
        if formAffectQuest.is_valid():
            formAffectQuest.save()
        else:
            formAffectQuest = AjoutQuestForm(patient=patient)
    else:
        formAffectQuest = AjoutQuestForm(patient=patient)

    ################# Form sequence
    if monPatient["sequence"] != None :
        print("tu peux créer un formulaire pour redefinir la séquence d'un patient !")
        maxValueOrdre=Ordre.objects.filter(sequence=monPatient["sequence"]).aggregate(maxOrdre=Max('ordre'))['maxOrdre']
        if request.method == "POST":
            print("tu peux créer un formulaire pour redefinir la séquence d'un patient !")
            if maxValueOrdre is not None:
                formS =OrdreForm(request.POST,sequence=monPatient["sequence"], maxOrdre=maxValueOrdre )
            else:
                formS =OrdreForm(request.POST,sequence=monPatient["sequence"], maxOrdre=0)
                if formS.is_valid():
                    formS.save()
                    formS.save_m2m()
                else:
                    if maxValueOrdre is not None:
                        formS =OrdreForm(sequence=monPatient["sequence"], maxOrdre=maxValueOrdre )
                    else:
                        formS =OrdreForm(sequence=monPatient["sequence"], maxOrdre=0)
        else:
            if maxValueOrdre is not None:
                formS =OrdreForm(sequence=monPatient["sequence"], maxOrdre=maxValueOrdre )
            else:
                formS =OrdreForm(sequence=monPatient["sequence"], maxOrdre=0)
        listOrdre = Ordre.objects.filter(sequence=monPatient["sequence"]).values('module__nom','ordre')
    else:
        listOrdre = None
        formS =None

    ############# Analyse
    AnalyseQuestM = enAttente.objects.filter(patient=patient, dateFin__isnull=False).values("module__pk", "module__nom","pk", "isAnalyse")

    ############# Gestion
    affectationQuestionnaire = enAttente.objects.filter(patient=patient,module__isQuestionnaireOnly=True, dateFin__isnull=True).values("module__nom", "module__pk", "ordreAtteint")
    if not affectationQuestionnaire.exists():
        affectationQuestionnaire=None

    ############# fin thérapie
    if request.method == 'POST':
        if request.POST.get("finTherapie") != None:
            pat = Patient.objects.get(pk=patient)
            pat.dateFinTherapie = timezone.now().date()
            pat.save()


    ################################################## Graphique ##################################################
    var=variableEtude.objects.all().values("pk","nom", "seuilMinimal", "seuilMaximal","seuilMoyen")

    return render(request, "user/clinicien/detail.html", {
        "monPatient":monPatient,
        "AnalyseQuestM":AnalyseQuestM,
        "formAffectQuest":formAffectQuest,
        "affectationQuestionnaire":affectationQuestionnaire,
        "agendaForm":formA,
        'newOrdre':formS,
        'listOrdre':listOrdre,
        'var':var,
        'idPatient':patient,
    })

######################################################## Send Resultat data per Graph

class sendDataDossier(View):
    def get(self, request, patient, variable):
        """
        Faire la moyenne des resultats si le meme jours de date de fin !
        """
        if (variable==0):
            dataset=Dossier.objects.filter(patient__pk=patient).values("resultat",Variable=F("variable__nom"), Date=F("enAttente__dateFin"))
        else:
            dataset=Dossier.objects.filter(patient__pk=patient, variable__pk=variable).values("resultat",Variable=F("variable__nom"), Date=F("enAttente__dateFin"))
        data= dict()
        data["variable"]=list(dataset)
        return JsonResponse(data)


########################################### Gestionnnaire

from .form import UserRegisterFrom, PatientRegisterFrom, GroupCreationForm, ClinicienRegisterFrom
from django.db.models import Count
@login_required
def Gestion(request):
    allClinicien = Clinicien.objects.all()
    allClinicien.annotate(nbPatient=Count('clinicien_du_patient'))
    allGroupe = Population.objects.filter(categorie__gt=1)
    formG = GroupCreationForm()
    print("{0}".format(PatientClinicienForm()),"{0}".format(PatientGroupForm(instance=allGroupe.first())))
    return render(request, "user/clinicien/gestionResponsable.html", {"GroupFrom": formG, "allClinicien":allClinicien, "allGroupe":allGroupe})

class GestionGroupe(View):
    def get(self, request, pkPop):
        form = PatientGroupForm(instance=Population.objects.get(pk=pkPop))
        return HttpResponse(form)

class GestionClinicien(View):
    def get(self, request, pkCli):
        form = PatientClinicienForm(instance=Clinicien.objects.get(pk=pkCli))
        return HttpResponse(form)
        
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
    return render(request, 'user/register/pt.html', {'formU': formU,'formP': formP})



def registerClinicien(request):
    ##Enregistremment patient
    if request.method =='POST':
        formU = UserRegisterFrom(request.POST)
        formC = ClinicienRegisterFrom(request.POST or None, request.FILES)
        if formU.is_valid() and formC.is_valid() :
            use = formU.save()
            cli = Clinicien.objects.create(user=use)
            if Population.objects.filter(categorie=1).exists():
            # Affecte un groupe categorie 1 de clinicien avec le moins de patient
                pop = Population.objects.filter(categorie=1).annotate(minCli=Count("integre")).first()
            else:
                #Creation d'un group et d'une population 
                group = Group.objects.create(name="Groupe catégorie 1 encore non-nommé numéro : {0}".format(Population.objects.filter(categorie=1).count()))
                group.save()
                pop = Population.objects.create(categorie=1,groupe=group)
                pop.save()
            cli.equipe = pop
            ClinicienRegisterFrom(request.POST, instance=cli).save()
            return redirect('login')
    else:
        formU = UserRegisterFrom()
        formC = ClinicienRegisterFrom()
    return render(request, 'user/register/cl.html', {'formU': formU,'formC': formC})