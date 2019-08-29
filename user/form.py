# https://metrogeek.fr/django-creer-formulaire/
from django import forms
from django.forms.widgets import TextInput

from .models import Population, Patient, Clinicien, Agenda, enAttente
from module.models import Module
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

from django.utils import timezone


#################################################################################################
################################### Enregistrement (patient view)###############################
#################################################################################################

########################################## User #############################################
class UserRegisterFrom(UserCreationForm):
    """
    Formulaire pour définition d'un nouvelle utilisateur, il est raccorder soit par un Patient soit un clinicien
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': "Nom d'utilisateur du site",
            'email': "Votre e-mail :",
            'password1': "Mot de passe",
            'password2': "Confirmer votre mot de passe :"
        }
########################################## Patient #############################################
class PatientRegisterFrom(forms.ModelForm):
    """
    Intégré dans la vue pt.html
    Ce formulaire crée un patient il est raccorder par UserResgisterForm
    """
    class Meta:
        model = Patient
        fields = ["universite", "parcours", 'telephone', "skype"]
        labels = {
            "universite": "Votre université : ",
            "parcours": "Dans quel parcours êtes vous ?",
            'telephone': "Votre numéro de téléphone :",
            'skype': "Veuillez donner votre nom d'utilisateur skype :"
        }
        widgets = {
            'telephone': TextInput(attrs={
                'type': 'tel',
                'class': "form-control",
                'placeholder': "Exemple : 0610101010",
                "Pattern": "/(\+\d+(\s|-))?0\d(\s|-)?(\d{2}(\s|-)?){4}/"
            }),
        }


########################################## Clincien #############################################
class ClinicienRegisterFrom(forms.ModelForm):
    """
        Intégré dans la vue cl.html
        Ce formulaire crée un clinicien il est raccorder par UserResgisterForm
        """
    class Meta:
        model = Clinicien
        fields = ["photoProfil"]
        labels = {
            "photoProfil": "Votre photo pour acquérir la confiance de vos patient "
        }


#################################################################################################
##################################### Interaction cli et patient ##############################
#################################################################################################

########################################## Agenda #############################################

class AgendaForm(forms.ModelForm):
    debut = forms.DateTimeField(initial=timezone.now(), label="Choissiez un moment :",
                                widget=TextInput(attrs={'type': 'datetime-local', 'class': "form-control"}))

    class Meta:
        model = Agenda
        fields = ['objet', 'debut', 'duree']
        labels = {
            'objet': 'Sujet de votre demande',
            'duree': 'Temps en heure et minutes',
        }
        widgets = {
            'objet': TextInput(attrs={'type': 'text', 'class': "form-control"}),
            'debut': TextInput(attrs={'type': 'datetime-local', 'class': "form-control"}),
            'duree': TextInput(attrs={'class': "form-control", "type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        self.clinicien = kwargs['clinicien']
        self.patient = Patient.objects.get(pk=kwargs['patient'])
        del kwargs['patient']
        del kwargs['clinicien']
        super(AgendaForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(AgendaForm, self).save(commit=False)
        print(self.patient, self.clinicien)
        instance.patient = self.patient
        instance.clinicien = self.clinicien
        if commit:
            instance.save()
        return instance


##########################################  Ajout de questionnaire #############################################
class AjoutQuestForm(forms.ModelForm):
    """
    Ajout d'un questionnaire au patient
    """
    module = forms.ModelChoiceField(queryset=None, to_field_name="pk",
                                    widget=forms.Select(attrs={'class': 'form-control'}), initial=0, required=True)

    class Meta:
        model = enAttente
        fields = ['module', 'repetition', 'dateVisible']
        labels = {
            'module': "Veuillez choisir un questionnaire",
            'repetition': 'Choisiez une periode de répétition du questionnaire : (en jour)',
            'dateVisible': "Choisissez la date où le questionnaire sera visible :",
        }
        help_texts = {
            'repetition': "Vous pouvez laisser vide ce champs ainsi le questionnaire ne sera fais qu'une fois"
        }

    def __init__(self, *args, **kwargs):
        self.patient = kwargs['patient']
        del kwargs['patient']
        super(AjoutQuestForm, self).__init__(*args, **kwargs)
        pkUseByPatient = enAttente.objects.filter(patient=self.patient, dateFin__isnull=True).values("module")
        self.fields["module"].queryset = Module.objects.filter(isQuestionnaireOnly=True, isVisible=True,
                                                               nbSection__gt=0).exclude(pk__in=pkUseByPatient)

    def save(self, commit=True):
        instance = super(AjoutQuestForm, self).save(commit=False)
        instance.patient = Patient.objects.get(pk=self.patient)
        if commit:
            instance.save()
        return instance


##############################################################################################################################
###################################### Gestion ###############################################################################
##############################################################################################################################

########################################## Manage clinicien #############################################
class PatientClinicienForm(forms.ModelForm):
    clinicien_du_patient = forms.ModelMultipleChoiceField(label="Patient n'étant pas à la charge du clinicien",
                                                          queryset=None, to_field_name="pk", initial=0)

    class Meta:
        model = Clinicien
        fields = ['clinicien_du_patient']

    def __init__(self, *args, **kwargs):
        self.clincien__pk = kwargs['clinicien']
        del kwargs['clinicien']
        super(PatientClinicienForm, self).__init__(*args, **kwargs)
        self.fields['clinicien_du_patient'].widget = forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
        self.fields["clinicien_du_patient"].queryset = Patient.objects.exclude(clinicienACharge__pk=self.clincien__pk)


########################################## Manage Population #############################################
class PatientPopulationForm(forms.ModelForm):
    patient = forms.ModelMultipleChoiceField(label="Patient ne faisant pas partie du groupe",
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


##########################################  Création Population #############################################
class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Population
        fields = ['categorie', "sequence", "lieu"]
        labels = {
            'categorie': 'Catégorie',
            "sequence": "Parcours utilisateur à definir",
            "lieu": "Population issue de"
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        labels = {
            'name': "Le nom du groupe :"
        }
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"})
        }
