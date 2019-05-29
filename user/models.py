#https://openclassrooms.com/fr/courses/1871271-developpez-votre-site-web-avec-le-framework-django/1873767-les-utilisateurs
from django.db import models
from django.contrib.auth.models import User



# Create your models here.
"""
class timeStampeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ## Permettre de rendre une class abstraite donc ne peut pas etre hériter !
    class Meta:
        abstract = True
"""

        

class user(User):
    nom = models.CharField(max_length=200)
    
    def __str__(self):
        return "Etudiant {0}".format(self.user.username)
"""
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    
class Journal(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    Patient  = models.ForeignKey(Patient, on_delete=models.CASCADE)
    
"""
