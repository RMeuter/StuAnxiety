#https://metrogeek.fr/django-creer-formulaire/
from django import forms
from django.forms.widgets import TextInput

from .models import Population, Patient, Clinicien, Message, Agenda, enAttente
from module.models import Module
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm

from django.utils import timezone

#################################################################################################
################################### Enregistrement (register view)###############################

########################################## User #############################################
class UserRegisterFrom(UserCreationForm):
    """
    Intégration d'un utilisateur lambda (clinicien ou patient)
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name' ,'email', 'password1', 'password2']
        labels = {
            'username': "Nom d'utilisateur du site", 
            'email': "Votre e-mail :", 
            'password1': "Mot de passe", 
            'password2': "Confirmer votre mot de passe :"
        }
        
########################################## Patient #############################################
class PatientRegisterFrom(forms.ModelForm):
    class Meta :
        model = Patient
        fields = ["universite","parcours", 'telephone',"skype"]
        labels ={
            "universite" : "Votre université : ",
            "parcours" : "Dans quel parcours êtes vous ?",
            'telephone':"Votre numéro de téléphone :",
            'skype':"Veuillez donner votre nom d'utilisateur skype :"
        }
        widgets = {
            'telephone': TextInput(attrs={'type': 'tel', 'class':"form-control", 'placeholder':"Exemple : 0610101010"},),#"pattern":"#^0[1-7][0-9]{8}$#"
        }

########################################## Clincien #############################################
class ClinicienRegisterFrom(forms.ModelForm):
    class Meta :
        model = Clinicien
        fields = ["photoProfil"]
        labels ={
            "photoProfil" : "Votre photo pour acquérir la confiance de vos patient "
        }



#################################################################################################
##################################### Interaction cli et patient ##############################


########################################## Agenda #############################################
        
class AgendaForm(forms.ModelForm):
    debut = forms.DateTimeField(initial = timezone.now(), widget=TextInput(attrs={'type': 'datetime-local', 'class':"form-control"}))
    class Meta:
        model=Agenda
        fields=['objet', 'debut', 'duree']
        labels = {
            'objet': 'Sujet de votre demande',
            'debut': 'Choissiez un moment :',
            'duree':'Temps en heure et minutes'
        }
        widgets = {
            'objet': TextInput(attrs={'type': 'text', 'class':"form-control"}),
            'duree': TextInput(attrs={'class':"form-control", "type":"time"}),
        }
        
    def __init__(self, *args, **kwargs):
        self.clinicien=kwargs['clinicien']
        self.patient=Patient.objects.get(pk=kwargs['patient'])
        del kwargs['patient']
        del kwargs['clinicien']
        super(AgendaForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super(AgendaForm, self).save(commit=False)
        print(self.patient,self.clinicien)
        instance.patient = self.patient
        instance.clinicien = pk=self.clinicien
        if commit:
            instance.save()
        return instance

########################################## Reprise de Message #############################################
    
class MessagerieForm(forms.ModelForm):
    """
    Voir pour un plug in de messagerie ! 
    """
    class Meta:
        model=Message
        fields=['message']
        labels={
            "message":""
        }
        widgets={
            'message': forms.Textarea(attrs={'class':"form-control"}),
        }
    def __init__(self, *args, **kwargs):
        self.patient=kwargs['patient']
        self.clinicien=kwargs['clinicien']
        del kwargs['patient']
        del kwargs['clinicien']
        super(MessagerieForm, self).__init__(*args, **kwargs)

##########################################  enAttente #############################################
class AjoutQuestForm(forms.ModelForm):
    """
    Ajout d'un questionnaire au patient
    """
    isRepetition=forms.BooleanField(required=False)
    Module=forms.ModelChoiceField(queryset=Module.objects.filter(isJournal=False, isQuestionnaireOnly=True), to_field_name="pk", widget=forms.Select(attrs={'class':'form-control'}), initial=0, required=True)
    class Meta:
        model=enAttente
        fields=['Module', 'repetition', 'dateVisible']
    def __init__(self, *args, **kwargs):
        self.patient=kwargs['patient']
        del kwargs['patient']
        super(AjoutQuestForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        instance = super(AjoutQuestForm, self).save(commit=False)
        instance.patient = Patient.objects.get(pk=self.patient)
        if commit:
            instance.save()
        return instance
###################################### Gestion Clinicien, groupe, ################################
        
########################################## clinicien #############################################
class PatientClinicienForm(forms.ModelForm):
    clinicien_du_patient = forms.ModelMultipleChoiceField(label="Patient n'étant pas à la charge du clinicien" ,queryset=None, to_field_name="pk", initial=0)
    class Meta:
        model=Clinicien
        fields=['clinicien_du_patient']
    def __init__(self, *args, **kwargs):
        self.clincien__pk = kwargs['clinicien']
        del kwargs['clinicien']
        super(PatientClinicienForm, self).__init__(*args, **kwargs)
        self.fields['clinicien_du_patient'].widget = forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
        self.fields["clinicien_du_patient"].queryset = Patient.objects.exclude(clinicienACharge__pk=self.clincien__pk)
########################################## Population #############################################
class PatientPopulationForm(forms.ModelForm):
    patient = forms.ModelMultipleChoiceField(label="Patient ne faisait pas partie du groupe",
                                                          queryset=None, to_field_name="pk", initial=0)
    class Meta:
        model = Population
        fields = ['patient']

    def __init__(self, *args, **kwargs):
        self.population__pk = kwargs['population']
        del kwargs['population']
        super(PatientPopulationForm, self).__init__(*args, **kwargs)
        self.fields['patient'].widget = forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
        self.fields["patient"].queryset = Patient.objects.exclude(groupePatients=self.population__pk)

########################################## Population #############################################
class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Population
        fields = ['categorie',  "sequence", "lieu"]
        labels = {
            'categorie': 'Catégorie', 
            "sequence": "Parcours utilisateur à definir",
            "lieu": "Population issue de"
        }
        