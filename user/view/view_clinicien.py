# Partie ajax
from django.http import JsonResponse
from django.views.generic import View
# Partie view
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
# Model et form propre au site
from user.models import Patient, Clinicien, Population, enAttente, Agenda, Group, variableEtude, Dossier
from user.form import AgendaForm, AjoutQuestForm, UserRegisterFrom, ClinicienRegisterFrom
from module.models import Ordre
from module.form import OrdreForm
# Requete et aggregat
from django.db.models import F, Sum, Max, Count
# Time
from django.utils import timezone




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
    return render(request, 'user/register/cl.html', {'formU': formU, 'formC': formC})


@login_required
@permission_required("user.parcours_Clinicien")
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
@permission_required("user.parcours_Clinicien")
def detail(request, patient):
    """
    Voir pour un object404 pour eviter que les cliniciens n'ailles sur les autre dossiers.
    Faire attention entre la différence entre le pk et uuci !
    """

    ############# Patient
    monPatient=get_object_or_404(Patient, pk=patient,clinicienACharge=request.user.clinicien).values("user__last_name", "user__first_name", "user__email", "telephone","skype", "sequence", "dateFinTherapie").get()
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
@login_required
@permission_required("user.parcours_Clinicien")
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

