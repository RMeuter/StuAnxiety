#https://openclassrooms.com/fr/courses/1871271-developpez-votre-site-web-avec-le-framework-django/1873767-les-utilisateurs
from django.db import models
from django.contrib.auth.models import User, Group



class Responsable(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hopital = models.CharField(max_length=200)
    def __str__(self):
        return "Responsable : {0} {1}".format(self.user.first_name,self.user.last_name)

class Praticiens(models.Model):
    reponsable = models.ForeignKey(Responsable,on_delete=models.CASCADE, blank=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    
class Clinicien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    praticiens  = models.ForeignKey(Praticiens, on_delete=models.CASCADE)
    hopital = models.CharField(max_length=200)
    def __str__(self):
        return "Psychologue : {0} {1}".format(self.user.first_name,self.user.last_name)

#-----------------------------------------------------------------------------------------------------    
    
class Universitaire(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    universitaire  = models.ForeignKey(Universitaire, on_delete=models.CASCADE)
    univ = models.CharField(max_length=200)
    def __str__(self):
        return "Etudiant : {0} {1}".format(self.user.first_name,self.user.last_name)
    
class Journal(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    patient  = models.ForeignKey(Patient, on_delete=models.CASCADE)
    reponse = models.CharField(max_length=200)
    def __str__(self):
        return "Etudiant {0} {1} a dit {2} à {3} ".format(patient.user.first_name,patient.user.last_name,self.reponse, self.created_at)
    

    