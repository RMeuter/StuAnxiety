from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, get_object_or_404, get_list_or_404
from django.views.generic import View, CreateView
from django.http import JsonResponse


from user.models import enAttente, Resultat, variableEtude
from module.models import Section, Module, Ordre, Sequence
from module.form import SondageForm, AnalyseForm


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.utils import timezone
from datetime import datetime

#####################################################################################################################################
def module(request, pk):
    """
    Lors de l'affichage de la vue du module sans la section nous verifions si le patient suivie bien sa sequence et qu'il n'utilise pas
    le code d'un autre module qui n'est pas enAttente dans la premiere condition if

    La seconde condition if nous verifions si l'utilisateur est un patient suivie afin de retrouver l'ordre qu'il avait laisser
    en dernier temps sinon il est affecter au début du module.
    """
    ##################################### Parcours sequentielle/ semi sequentielle
    if request.user.has_perm("module.Sequence_Individuel") or request.user.has_perm("module.Sequence_Groupal"):
        #################### Variable Patient
        patient = request.user.patient
        pkSequence = patient.get_sequence()
        ####################### Verification que le patient suivie bien son module -> sinon erreur 404
        if  Ordre.objects.filter(sequence=pkSequence).exists():
            get_object_or_404(enAttente, module=pk, patient=request.user.patient, dateFin__isnull=True, dateVisible__lte=timezone.now())
    ##################################### A tous utilisateur on affecte un ordre
    if request.user.has_perm("user.parcours_Patient_Suivie") and enAttente.objects.filter(module_id=pk, patient=request.user.patient,dateFin__isnull=True,dateVisible__lte=timezone.now()).exists():
        ordre = enAttente.objects.filter(module_id=pk, patient=request.user.patient,dateFin__isnull=True,dateVisible__lte=timezone.now()).values("ordreAtteint")[0]['ordreAtteint']
    else:
        ordre=1
    ##################################### Tous parcours !-> Module existant
    mod =get_object_or_404(Module, pk=pk, isVisible=True, nbSection__gt=0)
    return render(request, "module/Affiche/Module.html", {"module" : mod, "ordre":ordre})


################################################### Appel Ajax de la section

class Sectiondetail(View):
    """
    La vue regarde qu'elle type d'objet il va renvoyer il y a trois possibilités

    """
    def  get(self, request, ordre, module):
        """
        on intégre enAttente avec l'histoire d'ordre

        """
        ######################### Existance
        section = get_object_or_404(Section, ordre=ordre, module=module)
        ####### Variable
        nb_Section = section.module.nbSection

        #################################### Recuperation de l'ordre si le patient est suivie
        if request.user.has_perm("user.parcours_Patient_Suivie"):
            #### Variable d'interet
            patient=request.user.patient
            enAtt, create = enAttente.objects.get_or_create(patient=patient,module_id=module,dateFin__isnull=True)
            if create:
                print("Un objet en attente crée avec pour pk :", enAtt.pk)
            enAtt.ordreAtteint=ordre
            enAtt.save()
            print(enAtt.pk)
            request.session['enAttente']=enAtt.pk

            ##################################### Verification si le module est finit
            print("nb section :", nb_Section, "ordre :", ordre)
            if nb_Section==ordre:
                print("La fin est proche")
                enAtt.dateFin=datetime.today()
                enAtt.save()

                ####################### Verifie l'existance de module en attente encore
                if not enAttente.objects.filter(patient=patient, module__isQuestionnaireOnly=False, dateFin__isnull=True).exists():
                    print("Verifie s'il n'existe plus encore des modules dans enAttente")

                    ###################################### Diff de suivie
                    pkSequence = patient.get_sequence()
                    try :
                        if pkSequence :
                            print("passage réordonne")
                            try:
                                ######### On verifier que l'ordre +1 existe !
                                ordreObj = Ordre.objects.get(module=module, sequence=pkSequence)
                                print("verifie l'existance du module d'ordre + 1")
                                if Ordre.objects.filter(sequence=pkSequence, ordre=(ordreObj.ordre+1)).exists():
                                    position=ordreObj.ordre+1
                                    listeAdd = Ordre.objects.select_related("module").filter(sequence=pkSequence, ordre=position)
                                    print("Ajout des modules à enAttente")
                                    for moduleAdd in listeAdd :
                                        enAttente.objects.create(patient=patient, module=moduleAdd.module,ordreAtteint=0)
                                else :
                                    if request.user.has_perm("module.Sequence_Individuel"):
                                        print("supprimer l'ordre d'un patient semi-sequentielle ! Revoir ici")
                                        Sequence.objects.get(pk=pkSequence).possede.clear()
                                    elif request.user.has_perm("module.Sequence_Groupal"):
                                        print("A finit sa thérapie")
                                        request.user.dateFinTherapie=timezone.now()
                            except Ordre.DoesNotExist:
                                print("N'a pas d'ordre dans sa sequence")
                    except NameError:
                        print("Ne suis pas une séquence !")
                        
        #Integration du module ici
        if section.SectionType == 1 :
            return JsonResponse({"text":section.text})
        elif section.SectionType == 2 :
            formQ = SondageForm(question = section.question, enAttente=request.session["enAttente"])
            return JsonResponse({"question":"{0}".format(formQ), "inputType":section.question.inputType})
        elif section.SectionType == 3:
            return JsonResponse({"video":section.video, "titre":section.titre})


        
@method_decorator(csrf_exempt, name='dispatch')
class ReceveQuestion(CreateView):
    """
    checker si la derniere question à été effectuer !
    """
    def post(self, request, ordre, pk):
        
        question = get_object_or_404(Section, ordre=ordre, module=pk).question
        formQ = SondageForm(request.POST,question=question, enAttente=request.session["enAttente"])

        if request.user.has_perm("user.parcours_Patient_Suivie"):
            if formQ.is_valid():
                if question.isMultipleRep:
                    ins = formQ.save(commit=False)
                    ins.save()
                    formQ.save_m2m()
                else:
                    formQ.save()
                data= {"valide":True}
            else:
                data= {"valide":False}
        else:
            data= {"valide":True}
        return JsonResponse(data)


######################## Questionnaire reçu cli 
@login_required
def questionnaireAnalyse(request, pk):
    """

    :param request:
    :param pk: clé primaire d'une instance enAttente
    Fonction :
        Verifie si enAttente n'a pas déjà été traiter,
            Si non une liste les variables sur lequels se base le clinicien est crée

    :return: Une view d'analyse d'un questionnaire appartenant à un module finis en Attente d'analyse clinicien
    """
    ### Definition des varibles
    enAtt = enAttente.objects.get(pk=pk)
    patient= enAtt.patient
    ####### Construction des formulaires
    if enAtt.isAnalyse == False:
        listVariable = variableEtude.objects.all()
        ####### Verification de la présence de la méthode

        if request.method =='POST':
            OnePassage=False
            # Attention à l'ajout de variable au moment où met le formulaire et on le reçois
            indexVar=0
            for var in listVariable :
                formA =AnalyseForm({'resultat':request.POST.getlist("resultat")[indexVar]}, patient=patient, variable=var, enAttente=enAtt)
                if formA.is_valid():
                    formA.save()
                    if var.isImportante == True:
                        patient.lastScore = request.POST.get("resultat")[indexVar]
                        patient.save()
                    OnePassage=True
                indexVar+1
            if OnePassage:
                enAtt.isAnalyse=True
                enAtt.save()
                return redirect('detail', patient=patient.pk)
        else :
            ######################################### Création d'une suite de formulaire pour
            listVariableForm = []
            for var in listVariable :
                listVariableForm.append(AnalyseForm(patient=patient, variable=var, enAttente=enAtt))
        ########################################### Recuperation des questions qui sont enAttente pour le clinicien
        rep = Resultat.objects.filter(enAttente=enAtt, reponse__isnull=False).values("question__question", "reponse__reponse","created_at").order_by("question")
        repMuti = Resultat.objects.filter(enAttente=enAtt, reponses__isnull=False).values("question__question", "reponses__ManyReponses__reponse","created_at").order_by("question")
        repLibre = Resultat.objects.filter(enAttente=enAtt).exclude(reponseLibre="").values("question__question", "reponseLibre", "created_at")
        print(repMuti)
        return render(request, "module/Affiche/AnalyseQuestionnaire.html",
                      {'enAtt':enAtt,
                       "repLibre":repLibre,
                       "rep":rep,
                       "repMuti":repMuti,
                       "formVar":listVariableForm,
                       })
    else:
        return redirect('detail', patient=patient.pk)


def listModules(request):
    """
    Variable suite à la permission d'un suivie :
        - noOrdre : Booléan qui determine si le patient possède un ordre à respecter ou non
        - Patient : Model du patient utilisateur
        - pkSequence : reçu par l'appel d'une méthode Patient qui récupère le pk de sa Séquence de module concerné
    Fonction :
        Un premier if qui conserne les patient suivie avec une séquence définit.
            Le premier verifie s'il exite des modules en Attente
            Le second if verifier s'il n'a pas de module en attente de finission, et qu'il possède une séquence remplit
                Si c'est le cas il définit les premiers modules attribué à l'ordre 1
            Sinon il ne possède pas de module définis
            Une autre suite if s'il na pas de suite définis tous les modules sont attribué
            Sinon seulement les modules concerner au niveau de sa suite.
        S'il l'uitilsateur (patient et clinicien) n'a pas de séquence il peut voir tous les modules.
    """
    if request.user.has_perm( "module.Sequence_Groupal") or request.user.has_perm("module.Sequence_Individuel") :
        ################# Variable #########################
        noOrdre= False
        patient = request.user.patient
        pkSequence = patient.get_sequence()
        ################### Ici on effectue les vérifications ################################
        if enAttente.objects.filter(patient=patient, dateFin__isnull=True).exists():
            pass
        elif Ordre.objects.filter(sequence=pkSequence).exists() and not enAttente.objects.filter(patient=patient, dateFin__isnull=True).exists():
            print("Cree de modules dans enAttente car il ne possède aucun module enAttente")
            position=1
            listeAdd = Ordre.objects.filter(
                sequence=pkSequence,
                ordre=position,
                module__isVisible=True,
                module__nbSection__gt=0).values('module')
            for moduleAdd in listeAdd :
                enAttente.objects.create(patient=patient, module=moduleAdd.module,ordreAtteint=0)
        else :
            print("Pas de enAttente, ni de séquence faite")
            noOrdre=True
        ################### Ici on effectue les requetes après les vérifications ################################
        if noOrdre:
            print("Pas d'ordre 2")
            modules = get_list_or_404(Module, isVisible=True, nbSection__gt=0)
        else :
            print("Possede des modules")
            modules = get_list_or_404(Module,pk__in=enAttente.objects.filter(patient=patient,dateFin__isnull=True).values('module'),isVisible=True, nbSection__gt=0)

    else :
        modules = get_list_or_404(Module ,isVisible=True, isQuestionnaireOnly=False, nbSection__gt=0)
    return render(request, "module/Affiche/Modules.html", {'modules':modules})

