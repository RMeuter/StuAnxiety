from django import forms
from django.forms.widgets import TextInput

from .models import Reponse, Ordre, Module, Section, Question, Sequence
from user.models import Resultat, enAttente 

from django.utils.translation import gettext_lazy as _

############## Creation module

class ModuleForm (forms.ModelForm):
    questionnaireDependant = forms.ModelChoiceField(queryset =Module.objects.filter(isJournal=False, isQuestionnaireOnly=True), to_field_name="pk", widget=forms.Select(attrs={'class':'form-control'}), initial=0, required=False)
    class Meta:
        model = Module
        exclude= ('nbSection',)
        labels= {
            "nom":"Titre du module", "desc":"Description rapide de l'activité (pour le patient)",
            "image":"Icon pour representation", "isVisible":"Le module peut etre visible (cochez si oui)",
            "questionnaireDependant":"Possède t'il un questionnaire qui dépend du module seulement (à établir avant coup)"
        }

class SectionForm (forms.ModelForm):
    """    
    https://www.caktusgroup.com/blog/2018/05/07/creating-dynamic-forms-django/
    """
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

    def save(self, commit=True):
        instance = super(SectionForm, self).save(commit=False)
        instance.module = self.module
        if commit:
            instance.save()
        return instance
        
##################### Question Création par clinicien ###################

class QuestionForm(forms.ModelForm):
    class Meta :
        model  = Question
        fields='__all__'

                
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
            if self.question.inputType == 1 :
            ################################ Selection ########################################
                if  self.question.isMultipleRep:
                    self.fields['reponse'] = forms.ModelMultipleChoiceField(queryset =None, to_field_name="pk", initial=0)
                    self.fields['reponse'].widget = forms.SelectMultiple(attrs={'class':'form-control'})
                else : 
                    self.fields['reponse'] = forms.ModelChoiceField(queryset =None, to_field_name="pk", initial=0)
                    self.fields['reponse'].widget = forms.Select(attrs={'class':'form-control'})
            ################################ CheckBox ########################################
            elif self.question.inputType == 3 :
                self.fields['reponse'] = forms.ModelMultipleChoiceField(queryset =None, to_field_name="pk", initial=0)
                self.fields['reponse'].widget = forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'})
            ################################ Radio ########################################
            elif self.question.inputType == 2 :
                self.fields['reponse'] = forms.ModelChoiceField(queryset =None, to_field_name="pk", initial=0)
                self.fields['reponse'].widget = forms.RadioSelect(attrs={'class':'form-check-input'})
                
            ################################ Configuration ########################################
            self.fields['reponse'].label = self.question.question
            self.fields['reponse'].help_text = self.question.consigne
            self.fields['reponse'].queryset=Reponse.objects.filter(question=self.question.pk)
            del self.fields['reponseLibre']
        ####################################################################################################
        else :
        ####################################################################################################
            ################################ Question gradué ########################################
            if self.question.inputType == 5 :
                self.fields['reponseLibre'] = forms.IntegerField(widget=forms.widgets.NumberInput(attrs={'type':'range','class': 'form-control-range', 'step': '{0}'.format(self.question.intervaleGraduerInput)}))
            ################################ Question libre texte ########################################
            else:
                self.fields['reponseLibre'] = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", 'placeholder':self.question.consigne }))
            ################################ Configuration ########################################
            self.fields['reponseLibre'].help_text = self.question.consigne
            self.fields['reponseLibre'].label = self.question.question
            del self.fields['reponse']
            
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
