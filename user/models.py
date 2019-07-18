#https://openclassrooms.com/fr/courses/1871271-developpez-votre-site-web-avec-le-framework-django/1873767-les-utilisateurs
from django.db import models
from django.contrib.auth.models import User, Group
from module.models import Reponse, Module, Section, Questionnaire, Sequence, Question
from django.utils import timezone
from datetime import datetime

####################################### Affectation de Séquence ####################################### 

class variableEtude (models.Model):
    TYPE =[(1, "discrete"), (2, "continu")]
    typeStatistique = models.IntegerField(choices=TYPE) 
    nom = models.CharField(max_length=200, blank=True)
    
####################################### Groupe et user ####################################### 

class Responsable(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isClinicien = models.BooleanField(default=False)
    

class Population(models.Model):
    """
    Création de groupe de population pour différencier les permissions 
    Ajouter dynamiquement les permissions selon la catégorie derrière utiliser has_perms('permission') pour definir la gestion experimental
    """
    CATEGORIE = [(1, 'Equipe de clinicien'), (2, 'Groupe semi-séquentiel'),(3, 'Groupe séquentiel'), (4, 'Groupe non séquentiel'),  (5, 'Groupe non suivie')]
    categorie = models.IntegerField(choices=CATEGORIE)
    groupe = models.OneToOneField(Group, on_delete=models.CASCADE)
    lieu = models.CharField(max_length=200, blank=True, null=True)
    responsable = models.ForeignKey(Responsable,on_delete=models.SET_NULL,null=True, blank=True,related_name = 'a_pour_responsable')
    sequence = models.ForeignKey(Sequence,on_delete=models.SET_NULL,null=True, blank=True,related_name = 'admet_une_sequence_tel_que')
    def __str__(self):
        return "Groupe : {0} au nom de {1}".format(self.categorie, self.groupe.name)
    class Meta :
        ordering =["categorie"]
        permissions = (
            ('parcours_Clinicien', "Possibilité de parcours d'un clinicien"), # Groupe catégorie 1
            ('parcours_Patient_Suivie', "Possibilité de parcours d'un patient suivie"), # Groupe catégorie 2,3,4
            ('parcours_Patient_Non_Suivie', "Possibilité de parcours d'un patient non suivie") # Groupe catégorie 5
        )
    
    
    
class Clinicien(models.Model):
    """
    Ajouter une permission qui pourra lui accorder le titre de responsable clinicien
    Mettre un booléanField
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photoProfil = models.ImageField(upload_to="./Media/photosProfilsCliniciens/",default='CliniciensPics/image.png')
    equipe  = models.ForeignKey(Population, on_delete=models.SET_NULL,null=True, blank=True, related_name = 'integre')
    responsableEquipe  = models.ForeignKey(Responsable, on_delete=models.SET_NULL,null=True, blank=True, related_name = 'est_responsable_de')
    class Meta :
        ordering =["equipe"]
    def __str__(self):
        return "Psychologue : {0} {1}".format(self.user.first_name,self.user.last_name)
  
    

class Patient(models.Model):
    """
    Voir si on ne peut pas modifier pour mettre plusieur clinicien à charge
    
    Reflechir à un algorithme d'affectation
    """
    #----------------------------Model en OneToOne et ForeignKey-------------------------------------------
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groupePatients  = models.ForeignKey(Population, on_delete=models.SET_NULL, null=True)
    clinicienACharge  = models.ForeignKey(Clinicien, on_delete=models.CASCADE, null=True,blank=True, related_name = 'clinicien_du_patient')
    sequence = models.ForeignKey(Sequence,on_delete=models.SET_NULL,null=True, blank=True)
    #----------------------------Model propre au patient-------------------------------------------
    lastScore = models.IntegerField(blank=True, null=True)
    NoSeeMsgQuantity = models.IntegerField(default=0)
    universite = models.CharField(max_length=200)#Plus pour des études sociaulogique
    parcours = models.CharField(max_length=200)#Plus pour des études sociologique
    telephone = models.CharField(max_length=10,blank=True, null=True)
    skype = models.CharField(max_length=20, blank=True, null=True)
    point = models.IntegerField(default=0)
    dateFinTherapie = models.DateField(blank=True, null=True) 
    #----------------------------Model en ManyToMany-----------------------------------------------------
    questionnaire = models.ManyToManyField(Questionnaire, through="Parcours" )
    section = models.ManyToManyField(Section, through="Parcours")
    agenda = models.ManyToManyField(Clinicien, through="Agenda",related_name = 'Agenda')
    variable = models.ManyToManyField(variableEtude, through="Dossier")
    message = models.ManyToManyField(Clinicien, through="Message",related_name = 'Message')
    class Meta :
        ordering =["clinicienACharge","groupePatients"]
    def __str__(self):
        return "Etudiant : {0}".format(self.user.username)
    


####################################### Communication patient/ clinicien ####################################### 

class Message(models.Model):
    """
    Voir pour assembler message et agenda ?
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name = 'message_patient')
    clinicien = models.ForeignKey(Clinicien, on_delete=models.CASCADE, related_name = 'message_clinicien')
    message = models.CharField(max_length=255)
    isClinicien = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta :
        ordering =["patient", "created_at"]

class Agenda(models.Model):
    """
    Utilisation d'un graphe pour créneau agenda
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name = 'agenda_patient')
    clinicien = models.ForeignKey(Clinicien, on_delete=models.CASCADE, related_name = 'agenda_clini')
    objet = models.CharField(max_length=250)
    debut = models.DateTimeField(default=timezone.now)
    duree = models.DurationField(null=True)
    class Meta :
        ordering =["patient","debut"]
    def __str__(self):
        return "rdv de {0} avec {1} pour {2} ".format(self.patient.user.first_name,self.clinicien.user.last_name,self.objet)

####################################### Analyse parcours utilisateur ####################################### 

class Parcours (models.Model):
    """
    ManyToMany -> de Patient, Questionnaire, Agenda, Section
    Permet aussi de voir la progression ! selon un temps et ou est ce qu'il se situe
    
    Voir pour un graphe du parcours utilisateur et ainsi que la corrélation
    Prendre en compte les chevauchements pour un utilisateur qui fait deux tache à la fois
    
    Permettra de définir la loi d'un temps idéal à l'avenir !
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name = 'patient_parcours')
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True)
    entretien = models.ForeignKey(Clinicien, on_delete=models.CASCADE, blank=True, null=True, related_name = 'entretien')
    debut = models.DateTimeField(auto_now_add=True)
    duree = models.DurationField(null=True)#Peut etre null s'il n'est pas vraiment actif pendant 5 heures. 
    class Meta :
        ordering =["debut"]
    def get_parcours_by_day():
        pass
    def get_parcours():
        pass
    
class enAttente (models.Model):
    """
    Carrefour de l'affectation automatique du patient à travers son parcours expérimental
    """
    reponse = models.ManyToManyField(Reponse, through="Resultat")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, blank=True, null=True)
    ordreAtteint = models.SmallIntegerField(default=1)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, blank=True, null=True)
    repetition = models.PositiveSmallIntegerField(blank=True, null=True)
    dateVisible = models.DateField(default=timezone.now)
    forClinicien = models.BooleanField(default=False)
    isAnalyse = models.BooleanField(default=False)
    class Meta :
        ordering =["patient", "forClinicien","dateVisible"]
    def list_module_disponible():
        pass
    def list_questionnaire_disponible():
        pass
    def list_questionnaire_disponible_pour_clinicien():
        pass
    def __str__(self):
        if self.questionnaire !=None:
            return "en attente pour {0} avec {1}".format(self.patient, self.questionnaire)
        else:
            return "en attente pour {0} avec {1}".format(self.patient, self.module)
    

####################################### Trophé à voir par la suite ####################################### 

####################################### Gestion Données patient par clinicien ####################################### 


    
class Resultat(models.Model):
    """
    Un resultat d'une question donnée peut ou non contenir des reponses non cocher mais aussi libre et il est forcément est attribuer à un patient
    """
    enAttente = models.ForeignKey(enAttente, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    reponse = models.ForeignKey(Reponse, on_delete=models.CASCADE, blank=True, null=True)
    reponseLibre = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta :
        ordering =["enAttente","created_at"]
    def __str__(self):
        return "Patient {0} {1} a dit {2} à {3} ".format(self.enAttente.patient.user.first_name,self.enAttente.patient.user.last_name,self.reponse, self.created_at)
    
class Dossier(models.Model):
    """
    Voir pour le type d'un résultat
    Variable attribuer par le clinicien avec une date à la suite d'un questionnaire
    """
    variable = models.ForeignKey(variableEtude, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    resultat = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta :
        ordering =["created_at"]