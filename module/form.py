from django import forms
from .models import Reponse, Ordre, Module, Section, Questionnaire, Question, Sequence
from user.models import Resultat, enAttente 
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import TextInput

############## Creation module

class ModuleForm (forms.ModelForm):
    questionnaireDependant = forms.ModelChoiceField(queryset =Questionnaire.objects.filter(isJournal=False), to_field_name="pk", widget=forms.Select(attrs={'class':'form-control'}), initial=0, required=False)
    class Meta:
        model = Module
        exclude= ('nbSection',)
        labels= {"nom":"Titre du module", "desc":"Description rapide de l'activité (pour le patient)","image":"Icon pour representation", "isVisible":"Le module peut etre visible (cochez si oui)","questionnaireDependant":"Possède t'il un questionnaire qui dépend du module seulement (à établir avant coup)"}

class SectionForm (forms.ModelForm):
    """    
    https://www.caktusgroup.com/blog/2018/05/07/creating-dynamic-forms-django/"""
    video =forms.CharField( help_text="Veuillez recupérér le code en gras dans l'url suivant :https://www.youtube.com/watch?v=<strong>eWX73LqwHxg</strong>")
    class Meta:
        model = Section
        exclude= ('module',)
        widgets = {
            'ordre': forms.HiddenInput(),
            'video': TextInput()
        }
        
    def __init__(self,typeS="Q", *args, **kwargs):
        self.module = kwargs['module']
        del kwargs['module']
        super(SectionForm, self).__init__(*args, **kwargs)
        if typeS=="Q":
            """
            Reutilisation de la méthode de groupe et patient
            On garde l'instance et on prend le pk puis on l'ajoute
            """
            del self.fields['text']
            del self.fields['video']
        elif typeS=="T":
            del self.fields['question']
            del self.fields['video']
        elif typeS=="V":
            del self.fields['question']
            del self.fields['text']

    def save(self, commit=True):
        instance = super(SectionForm, self).save(commit=False)
        instance.module = self.module
        if commit:
            instance.save()
        return instance
        
##################### Questionnaire ###################

class QuestionnaireForm(forms.ModelForm):
    class Meta :
        model  = Questionnaire
        exclude= ('nbQuestion',) 
        labels ={"nom": "Titre du questionnaire","isVisible":"Le questionnaire peut etre visible (cochez si oui)","isJournal":"Es-ce que le questionnaire sera répéter (cochez si oui) ou sera éphémère et dependera d'un module"}
        

class QuestionForm(forms.ModelForm):
    class Meta :
        model  = Question
        exclude= ('questionnaire',)
    def __init__(self, *args, **kwargs):
        self.questionnaire = kwargs['questionnaire']
        del kwargs['module']
        super(SectionForm, self).__init__(*args, **kwargs)

##################### Sequence ########################
        
class OrdreForm (forms.ModelForm):
    """
    Permet d'ajouter un module à la liste 
    """
    module=forms.ModelChoiceField(queryset =Module.objects.filter(isVisible=True,nbSection__gt=0), to_field_name="pk", widget=forms.Select(attrs={'class':'form-control'}), initial=0)
    ordre = forms.NumberInput(attrs={'class':"form-control"})
    class Meta :
        model = Ordre
        fields = ('module', 'ordre')
        
    def __init__(self, *args, **kwargs):
        """
        Ce formulaire n'est disponible que dans deux cas :
        - gestion groupal : sequentielle
        - gestion patient : semi sequentielle
        """
        self.sequence=Sequence.objects.get(pk=kwargs['sequence'])
        del kwargs['sequence']
        maxOrdre = kwargs['maxOrdre']
        del kwargs['maxOrdre']
        super(OrdreForm, self).__init__(*args, **kwargs)
        """
        Attention au changement de dernière minute par le clinicien !
        """
        self.fields['ordre'].widget.attrs['max']=1+maxOrdre
        self.fields['ordre'].widget.attrs['min']=1
    
    def save(self, commit=True):
        instance = super(OrdreForm, self).save(commit=False)
        instance.sequence = self.sequence
        if commit:
            instance.save()
        return instance
        
################################# Questionnaire pour le patient ####################
class SondageForm (forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        inspiré de 
        https://stackoverflow.com/questions/42745403/use-required-attribute-missing-1-required-positional-argument-initial-djang
        https://www.programcreek.com/python/example/52461/django.forms.ModelChoiceField
        https://getbootstrap.com/docs/4.3/components/forms/ -> pour design
        https://docs.djangoproject.com/en/2.2/ref/forms/widgets/
        """
        self.question=kwargs['question']
        self.enAttente=enAttente.objects.get(pk=kwargs['enAttente'])
        del kwargs['question']
        del kwargs['enAttente']
        super(SondageForm, self).__init__(*args, **kwargs)
        ## reste reponse -> FK , reponseLibre -> texteArea
        ## choix intégration : reponse, reponseLibre
        if self.question.inputType <4 :
            if  self.question.isMultipleRep:
                self.fields['reponse'] = forms.ModelMultipleChoiceField(queryset =None, to_field_name="pk", initial=0)
                if self.question.inputType == 1 : self.fields['reponse'].widget = forms.SelectMultiple(attrs={'class':'form-control'})
                else : self.fields['reponse'].widget = forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'})
            else :
                self.fields['reponse'] = forms.ModelChoiceField(queryset =None, to_field_name="pk", initial=0)
                if self.question.inputType == 1 : self.fields['reponse'].widget = forms.Select(attrs={'class':'form-control form-control-sm'})
                else: self.fields['reponse'].widget = forms.RadioSelect(attrs={'class':'form-check-input'})
            
            self.fields['reponse'].label = self.question.question
            self.fields['reponse'].queryset=Reponse.objects.filter(question=self.question.pk)
            del self.fields['reponseLibre']
            """
            if analyse==True:
                self.fields['reponse'].required = False
                self.fields['reponse'].widget.attrs['disabled'] = 'disabled'
            """
        else :
            if self.question.intervaleGraduerInput > 0:
                self.fields['reponseLibre'] = forms.IntegerField(help_text=self.question.consigne,widget=forms.widgets.NumberInput(attrs={'type':'range','class': 'form-control-range', 'step': '{0}'.format(self.question.intervaleGraduerInput)}))
            else:
                self.fields['reponseLibre'] = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", 'placeholder':self.question.consigne }))
            self.fields['reponseLibre'].label = self.question.question
            del self.fields['reponse']
            """
            if analyse==True:
                self.fields['reponseLibre'].required = False
                self.fields['reponseLibre'].widget.attrs['readonly'] = True
            """
    class Meta :
        model = Resultat
        exclude= ('created_at', 'question', 'enAttente') 
        
    def save(self, commit=True):
        instance = super(SondageForm, self).save(commit=False)
        instance.enAttente = self.enAttente
        instance.question = self.question
        if commit:
            instance.save()
        return instance
