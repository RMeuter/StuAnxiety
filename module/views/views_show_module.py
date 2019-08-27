from django.shortcuts import render,redirect, get_object_or_404, get_list_or_404
from module.form import SondageForm, AnalyseForm

from django.http import JsonResponse

from user.models import enAttente, Resultat, variableEtude
from module.models import Section, Module, Ordre, Sequence

from django.views.generic import View, CreateView

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.
# https://www.techiediaries.com/python-django-ajax/
# https://forum.alsacreations.com/topic-1-76028-1-Pdf-a-afficher-sur-page-Web.html


from django.utils import timezone
from datetime import datetime

#####################################################################################################################################
def module(request, pk):
    """
    Verifier s'il correspond à celui e liste d'attente
    if in list attente -> possible -> et utiliser l'ordre pour l'appel
    else -> redirect list module
    """
    ##################################### Parcours sequentielle/ semi sequentielle
    patient = request.user.patient
    if request.user.has_perm("module.Sequence_Individuel") or request.user.has_perm("module.Sequence_Groupal"):
        pkSequence = patient.get_sequence()
        if  Ordre.objects.filter(sequence=pkSequence).exists():
            get_object_or_404(enAttente, module=pk, patient=request.user.patient, dateFin__isnull=True, dateVisible__lte=timezone.now())

    ##################################### Tous parcours !-> Ordre
    ordre = enAttente.objects.filter(module_id=pk, patient=request.user.patient,dateFin__isnull=True,dateVisible__lte=timezone.now()).values("ordreAtteint")
    if ordre.exists():
        ordre = ordre[0]['ordreAtteint']
    else:
        ordre=1
    ##################################### Tous parcours !-> Module existant
    mod =get_object_or_404(Module, pk=pk, isVisible=True, nbSection__gt=0)
    return render(request, "module/Affiche/Module.html", {"module" : mod, "ordre":ordre})



##############################

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
        patient=request.user.patient
        nb_Section = Module.objects.get(pk=module).nbSection
        
        #################################### Recuperation de l'ordre selon leur suivie
        if request.user.has_perm("user.parcours_Patient_Suivie") or request.user.has_perm("user.parcours_Patient_Non_Suivie"):
            enAtt, create = enAttente.objects.get_or_create(patient=patient,module_id=module,dateFin__isnull=True)
            enAtt.ordreAtteint=ordre
            enAtt.save()
            print(enAtt.pk)
            request.session['enAttente']=enAtt.pk
            
            ##################################### Verification si le module est finit
            
            if nb_Section==ordre:
                print("La fin est proche")
                enAtt.dateFin=datetime.today()
                enAtt.save()
                
                ####################### Verifie l'existance de module en attente encore
                if not enAttente.objects.filter(patient=patient, module__isQuestionnaireOnly=False, dateFin__isnull=True).exists():
                    print("Verifie s'il n'existe plus encore des modules dans enAttente")
                    
                    ###################################### Diff de suivie
                    if request.user.has_perm("module.Sequence_Individuel"):
                        print("premier passage indiv")
                        pkSequence=request.user.patient.sequence.pk
                    elif request.user.has_perm("module.Sequence_Groupal"):
                        print("passage groupe")
                        pkSequence=request.user.patient.groupePatients.sequence.pk
                    try :
                        if pkSequence :
                            print("passage réordonne")
                            try:
                                ######### On verifier que l'ordre +1 existe !
                                ordreObj = Ordre.objects.get(module=module, sequence=pkSequence)
                                print(ordreObj)
                                if Ordre.objects.filter(sequence=pkSequence, ordre=(ordreObj.ordre+1)).exists():
                                    print("Ajout des modules à enAttente")
                                    """
                                    verifie l'existance du module d'ordre + 1
                                    """
                                    position=ordreObj.ordre+1
                                    listeAdd = Ordre.objects.select_related("module").filter(sequence=pkSequence, ordre=position)
                                    for moduleAdd in listeAdd :
                                        enAttente.objects.create(patient=patient, module=moduleAdd.module,ordreAtteint=0)
                                else :
                                    """
                                    Ce else est archi important car il détermine la fin de la thérapie si ordre +1 n'existe pas pour les groupe
                                    séquentielle
                                    pour les semi séquentielle eux on surpprime toutes leur sequences et il auront accès à tous !
                                    Voir
                                    """
                                    if request.user.has_perm("module.Sequence_Individuel"):
                                        print("supprimer l'ordre d'un patient semi-sequentielle !")
                                        Sequence.objects.get(pk=pkSequence).possede.clear()
                                    elif request.user.has_perm("module.Sequence_Groupal"):
                                        print("A finit sa thérapie")
                                        request.user.dateFinTherapie=timezone.now()
                            except Ordre.DoesNotExist:
                                print("N'a pas d'ordre dans sa sequence")
                    except NameError:
                        print("Ne suis pas une séquence !")
                        
        #Integration du module ici
        print(section.SectionType)
        if section.SectionType == 1 :
            return JsonResponse({"text":section.text})
        elif section.SectionType == 2 and request.user.has_perm("user.parcours_Patient_Suivie"):
            formQ = SondageForm(question = section.question, enAttente=request.session["enAttente"])
            return JsonResponse({"question":"{0}".format(formQ)})
        elif section.SectionType == 2 and not request.user.has_perm("user.parcours_Patient_Suivie"):
            return get(self, request, ordre+1, module)
        elif section.SectionType == 3:
            return JsonResponse({"video":section.video, "titre":section.titre})


        
@method_decorator(csrf_exempt, name='dispatch')
class ReceveQuestion(CreateView):
    """
    checker si la derniere question à été effectuer !
    https://stackoverflow.com/questions/4684618/django-modelmultiplechoicefield-wont-save-data
    """
    def post(self, request, ordre, pk):
        
        question = get_object_or_404(Section, ordre=ordre, module=pk).question
        formQ = SondageForm(request.POST,question=question, enAttente=request.session["enAttente"])
        
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
        return JsonResponse(data)


######################## Questionnaire reçu cli 

def questionnaireAnalyse(request, pk):
    """
    Deux types :
        - M pour question issue d'un module
    """
    ### Definition des varibles
    enAtt = enAttente.objects.get(pk=pk)
    patient= enAtt.patient
    if enAtt.isAnalyse == False:
        ####### Construction des formulaires
        listVariable = variableEtude.objects.all()
        if request.method =='POST':
            OnePassage=False
            # Attention à l'ajout de variable au moment où met le formulaire et on le reçois
            print(request.POST)
            indexVar=0
            for var in listVariable :
                formA =AnalyseForm({'resultat':request.POST.getlist("resultat")[indexVar]}, patient=patient, variable=var, enAttente=enAtt)
                if formA.is_valid():
                    formA.save()
                    if var.isImportante == True:
                        patient.lastScore = request.POST.get("resultat")[indexVar]
                        patient.save()
                    OnePassage=True
                indexVar+=1
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
        repLibre = Resultat.objects.filter(enAttente=enAtt).exclude(reponseLibre="").values("question__question", "reponseLibre", "created_at")

        return render(request, "module/Affiche/AnalyseQuestionnaire.html",
                      {'enAtt':enAtt,
                       "repLibre":repLibre,
                       "rep":rep,
                      "formVar":listVariableForm
                      })
    else:
        return redirect('detail', patient=patient.pk)


#https://docs.djangoproject.com/fr/2.2/topics/class-based-views/generic-editing/


def listModules(request):
    """
        https://www.sitepoint.com/best-html-wysiwyg-plugins/
        https://quilljs.com/docs/quickstart/
        https://djangopackages.org/grids/g/wysiwyg/
        https://techwiser.com/best-wysiwyg-html-editor-open-source/
    Il faut verifier l'appartenance au groupe et donner ce qu'il y a en attente.
    https://docs.djangoproject.com/fr/2.2/ref/models/expressions/#value-expressions
    """
    if request.user.has_perm( "module.Sequence_Groupal") or request.user.has_perm("module.Sequence_Individuel") :
        """
        module filter par en attente !
        attention au dernier module 
        """
        noOrdre= False
        patient = request.user.patient
        pkSequence = patient.get_sequence()

        if Ordre.objects.filter(sequence=pkSequence).exists() and not enAttente.objects.filter(patient=patient, dateFin__isnull=True).exists():
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

