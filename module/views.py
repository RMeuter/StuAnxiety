from django.shortcuts import render,redirect, get_object_or_404, get_list_or_404
from .form import SondageForm, QuestionnaireForm, ModuleForm, QuestionForm, SectionForm
# Utilisation d'ajax
from django.http import JsonResponse, HttpResponse, FileResponse

from user.models import Patient, Clinicien, User, Population, Group, enAttente, Resultat 
from .models import Section, Module, Ordre, Sequence,  Question, Reponse, Questionnaire

from django.views.generic import View, CreateView


# Create your views here.
# https://www.techiediaries.com/python-django-ajax/
# https://forum.alsacreations.com/topic-1-76028-1-Pdf-a-afficher-sur-page-Web.html


from django.utils import timezone

#####################################################################################################################################
def module(request, pk):
    """
    Verifier s'il correspond à celui e liste d'attente
    if in list attente -> possible -> et utiliser l'ordre pour l'appel
    else -> redirect list module
    """
    ##################################### Parcours sequentielle/ semi sequentielle
    if request.user.has_perm("module.Sequence_Individuel") or request.user.has_perm("module.Sequence_Groupal"):
        if request.user.has_perm("module.Sequence_Individuel"):
            pkSequence=request.user.patient.sequence.pk
        elif request.user.has_perm("module.Sequence_Groupal"):
            pkSequence=request.user.patient.groupePatients.sequence.pk
        if  Ordre.objects.filter(sequence=pkSequence).exists():
            get_object_or_404(enAttente, module=pk, patient=request.user.patient, forClinicien=False, dateVisible__lte=timezone.now())
            
    ##################################### Tous parcours !-> Ordre
    ordre = enAttente.objects.filter(module_id=pk, patient=request.user.patient,forClinicien=False,dateVisible__lte=timezone.now()).values("ordreAtteint")
    if ordre.exists():
        ordre = ordre[0]['ordreAtteint']
    else:
        ordre=1
    ##################################### Tous parcours !-> Module existant
    mod =get_object_or_404(Module, pk=pk, isVisible=True, nbSection__gt=0)
    return render(request,"module/Affiche/Module.html", {"module" : mod, "ordre":ordre})



##############################
def questionnaireAnalyse(request, pk):
    """
    Deux types : 
        - M pour question issue d'un module 
        - Q pour question issue d'un questionnaire 
    """
    
    enAtt = enAttente.objects.get(pk=pk)
    ########################################### Recuperation des questions qui sont enAttente pour le clinicien
    rep = Resultat.objects.filter(enAttente=enAtt, reponse__isnull=False).values("question__question", "reponse__reponse","created_at").order_by("question")
    repLibre = Resultat.objects.filter(enAttente=enAtt, reponseLibre__isnull=False).values("question__question", "reponseLibre", "created_at")
    
    print(rep)
    print(repLibre)
    return render(request, "module/Affiche/AnalyseQuestionnaire.html", {'enAtt':enAtt, "repLibre":repLibre, "rep":rep})


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
            enAtt = enAttente.objects.get_or_create(patient=patient,module_id=module,forClinicien=False)
            enAtt.ordreAtteint=ordre
            enAtt.save()
            request.session['enAttente']=enAtt[0].pk
            print(enAtt.pk)
            
            ##################################### Verification si le module est finit
            
            if nb_Section==ordre:
                print("La fin est proche")
                enAtt.forClinicien=True
                enAtt.save()
                
                ####################### Verifie l'existance de module en attente encore
                if not enAttente.objects.filter(patient=patient,isQuestionnaireOnly=False, forClinicien=False).exists():
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
                            except Ordre.DoesNotExist:
                                print("Bug dans la matrice !")
                    except NameError:
                        print("Ne suis pas une séquence !")
                        
        #Integration du module ici
        if section.question != None and request.user.has_perm("user.parcours_Patient_Suivie"):
            formQ = SondageForm(question = section.question, enAttente=request.session["enAttente"])
            return JsonResponse({"question":"{0}".format(formQ)})
        elif section.question != None and not request.user.has_perm("user.parcours_Patient_Suivie"):
            return get(self, request, ordre+1, module)
        elif section.video  != None:
            return JsonResponse({"video":section.video, "titre":section.titre})
        else :
            return JsonResponse({"text":section.text})


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
        
@method_decorator(csrf_exempt, name='dispatch')
class ReceveQuestion(CreateView):
    """
    checker si la derniere question à été effectuer !
    https://stackoverflow.com/questions/4684618/django-modelmultiplechoicefield-wont-save-data
    """
    def post(self, request,typeQ, ordre, pk):
        if typeQ=="M":
            question = get_object_or_404(Section, ordre=ordre, module=pk).question
        else:
            data['error'] =  "form not valid!"
            question = get_object_or_404(Question, ordre=ordre, questionnaire=pk)
        
        print('Tu es passer gros !')
        if question.isMultipleRep:
            print('is multi')
            formQ = SondageForm({"reponse":[1, 2]} ,question=question, enAttente=request.session["enAttente"])
            print(formQ)
            for rep in request.POST.get('reponse'):
                data = {'reponse':rep}
                formQ = SondageForm( data ,question=question, enAttente=request.session["enAttente"])
                print(formQ)
                if formQ.is_valid():
                    formQ.save()
                    formQ.save_m2m()
        else :
            formQ = SondageForm(request.POST,question=question, enAttente=request.session["enAttente"])
            print(formQ)
        ##### Ici ça marche
            if formQ.is_valid():
                print('No multi')
                formQ.save(commit=True)
                formQ.save_m2m()
                data= {"valide":True}
            else:
                data= {"valide":False}
        return JsonResponse(data)


######################## Questionnaire reçu cli 


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
        
        if request.user.has_perm("module.Sequence_Individuel"):
            pkSequence=request.user.patient.sequence.pk
        elif request.user.has_perm("module.Sequence_Groupal"):
            pkSequence=request.user.patient.groupePatients.sequence.pk
            
        if enAttente.objects.filter(patient=patient, isQuestionnaireOnly=False).exists():
            print("Possède des modules en attente")
            modules = enAttente.objects.select_related("module").filter(patient=patient)
        elif Ordre.objects.filter(sequence=pkSequence).exists() :
            print("Cree de modules dans enAttente")
            print(Ordre.objects.filter(sequence=pkSequence))
            position=1
            listeAdd = Ordre.objects.select_related("module").filter(sequence=pkSequence, ordre=position)
            for moduleAdd in listeAdd :
                enAttente.objects.create(patient=patient, module=moduleAdd.module,ordreAtteint=0)
        else :
            print("Pas d'ordre")
            noOrdre=True
        #Si rien n'est effectuer le patient voit tous les modules !
        if noOrdre:
            print("Pas d'ordre 2")
            modules = Module.objects.filter(isVisible=True, nbSection__gt=0)
        else :    
            print("Possede un ordre")
            modules = Module.objects.filter(pk__in=enAttente.objects.filter(patient=patient,forClinicien=False).values('module'),isVisible=True, nbSection__gt=0)
    else :
        modules = Module.objects.filter(isVisible=True, nbSection__gt=0)
    return render(request, "module/Affiche/Modules.html", {'modules':modules})
    
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################


##################### Creation !

def alterModules(request):
    """
    Crée deux liste une d'un formulaire et l'autre de questionnaire
    Ajoute un formulaire qui redirige vers une page de création de section
    Deux form de creation : questionnaire et module
    La liste des modules et questionnaires
    """
    if request.method == "POST":
        formM = ModuleForm(request.POST, request.FILES)
        if formM.is_valid():
            module = formM.save()
            print('AlterPart/')
            return redirect('AlterPart/Crea/Mod/{0}/1'.format(module.pk))
    else:
        formM = ModuleForm()
    listeModule = Section.objects.select_related("module").all().order_by('module__id', 'ordre').values("module__nom","module__desc","module__image","module__questionnaireDependant",'ordre',"titre")
    return render(request, "module/Alter/AlterModules.html", {"formM":formM,'modules':listeModule})

def alterQuestionnaire(request):
    if request.method=="POST":
        formQ = QuestionnaireForm(request.POST)
        if formQ.is_valid():
            questionnaire = formQ.save()
            return redirect('AlterPart/Crea/Quest/{0}/1'.format(questionnaire.pk))
    else:
        formQ = QuestionnaireForm()
    listeQuestionnaire = Question.objects.select_related("questionnaire").filter(questionnaire__isnull=False).order_by('questionnaire__id','ordre').values('questionnaire__nom','questionnaire__isJournal','question','ordre')
    return render(request, "module/Alter/AlterQuestionnaire.html", {"formQ":formQ,"questionnaire":listeQuestionnaire})
    
    
    
    
    
    
    

def alterActivy(request, creation="Crea", typeActivity="Mod", pkActivity=1,ordreIn=1):
    """
    Modifie ou crée : question ou section
    """
    if creation != "Crea":
        if typeActivity == "Quest":
            return render(request, "module/Alter/AlterActivity.html", {})
        elif typeActivity == "Mod":
            return render(request, "module/Alter/AlterActivity.html", {})
    else :
        if typeActivity == "Quest":
            return render(request, "module/Alter/AlterActivity.html", {})
        elif typeActivity == "Mod":
            return render(request, "module/Alter/AlterActivity.html", {})

class EnvoieDifferentForm(View):
    def get(self, request, formList, pkModif=None):
        if pkModif == None :
            if listFormQuest[formList]["typeF"] == "S":
                form = SectionForm(typeS=listFormQuest[formList])
            else:
                form = QuestionForm(typeQ=formList)
        elif typeof(pkModif)==int :
            if listFormQuest[formList]["typeF"] == "S":
                form = SectionForm(typeS=listFormQuest[formList], instance=pkModif)
            else :
                form = QuestionForm(typeQ=formList,instance=pkModif)
        else :
            form=None
        return HttpResponse(form)
            