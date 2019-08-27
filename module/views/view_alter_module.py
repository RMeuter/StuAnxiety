from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import HttpResponse

from module.form import ModuleForm, QuestionForm, SectionForm
from module.models import Section


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
    listeModule = Section.objects.select_related("module").all().order_by('module__id', 'ordre').values("module__nom",
                                                                                                        "module__desc",
                                                                                                        "module__image",
                                                                                                        "module__questionnaireDependant",
                                                                                                        'ordre',
                                                                                                        "titre")

    return render(request, "module/Alter/AlterModules.html", {"formM": formM, 'modules': listeModule})


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
        listFormQuest = []
        if pkModif == None :
            if listFormQuest[formList]["typeF"] == "S":
                form = SectionForm(typeS=listFormQuest[formList])
            else:
                form = QuestionForm(typeQ=formList)
        elif pkModif==int :
            if listFormQuest[formList]["typeF"] == "S":
                form = SectionForm(typeS=listFormQuest[formList], instance=pkModif)
            else :
                form = QuestionForm(typeQ=formList,instance=pkModif)
        else :
            form=None
        return HttpResponse(form)
