#https://metrogeek.fr/django-creer-formulaire/
from django import forms
from django.forms.widgets import TextInput, NumberInput
from .models import Population, Patient, Clinicien, Message, Agenda, enAttente
from module.models import Questionnaire
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

################## Enregistrement (register view)

class UserRegisterFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name' ,'email', 'password1', 'password2']
        labels = {'username': "Nom d'utilisateur du site", 'email': "Votre e-mail :", 'password1': "Mot de passe", 'password2': "Confirmer votre mot de passe :"}
        
class PatientRegisterFrom(forms.ModelForm):
    class Meta :
        model = Patient
        fields = ["universite","parcours", 'telephone',"skype" ]
        labels ={"universite" : "Votre université : ","parcours" : "Dans quel parcours êtes vous ?", 'telephone':"Votre numéro de téléphone :",'skype':"Veuillez donner votre nom d'utilisateur skype :"}
        widgets = {
            'telephone': TextInput(attrs={'type': 'tel', 'class':"form-control", 'placeholder':"Exemple : 0610101010"},),#"pattern":"#^0[1-7][0-9]{8}$#"
        }

class ClinicienRegisterFrom(forms.ModelForm):
    class Meta :
        model = Clinicien
        fields = ["photoProfil","responsableEquipe" ]
        labels ={"photoProfil" : "Votre photo pour acquérir la confiance de vos patient ","responsableEquipe" : "Votre responsable en d'équipe :"}



##################################### Interaction cli et patient ##############################
        
class AgendaForm(forms.ModelForm):
    debut = forms.DateTimeField(initial = timezone.now(), widget=TextInput(attrs={'type': 'datetime-local', 'class':"form-control"}))
    class Meta:
        model=Agenda
        fields=['objet', 'debut', 'duree']
        labels = {'objet': 'Sujet de votre demande','debut': 'Choissiez un moment :', 'duree':'Temps en heure et minutes'}
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

    
class MessagerieForm(forms.ModelForm):
    class Meta:
        model=Message
        fields=['message']
        labels={"message":""}
        widgets={
            'message': forms.Textarea(attrs={'class':"form-control"}),
        }
    def __init__(self, *args, **kwargs):
        self.patient=kwargs['patient']
        self.clinicien=kwargs['clinicien']
        del kwargs['patient']
        del kwargs['clinicien']
        super(MessagerieForm, self).__init__(*args, **kwargs)
        
class AjoutQuestForm(forms.ModelForm):
    isRepetition=forms.BooleanField(required=False)
    questionnaire=forms.ModelChoiceField(queryset=Questionnaire.objects.filter(isJournal=False), to_field_name="pk", widget=forms.Select(attrs={'class':'form-control'}), initial=0, required=True)
    class Meta:
        model=enAttente
        fields=['questionnaire', 'repetition', 'dateVisible']
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
        
class PatientClinicienForm(forms.ModelForm):
    clinicien_du_patient=forms.ModelMultipleChoiceField(queryset=Patient.objects.all().order_by('clinicienACharge'), to_field_name="pk", widget=forms.SelectMultiple(attrs={'class':'form-control'}), initial=0, required=True)
    class Meta:
        model=Clinicien
        fields=['clinicien_du_patient']
    def __init__(self, *args, **kwargs):
        super(PatientClinicienForm, self).__init__(*args, **kwargs)

class PatientGroupForm(forms.ModelForm):
    patient=forms.ModelMultipleChoiceField(queryset=Patient.objects.all().order_by('groupePatients'), to_field_name="pk", widget=forms.SelectMultiple(attrs={'class':'form-control'}), initial=0, required=True)
    class Meta:
        model=Population
        fields=['patient']
    def __init__(self, *args, **kwargs):
        super(PatientGroupForm, self).__init__(*args, **kwargs)

class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Population
        fields = ['categorie',  "sequence", "lieu"]
        labels = {'categorie': 'Catégorie', "sequence": "Parcours utilisateur à definir", "lieu": "Population issue de"}
        