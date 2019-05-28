from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.

        
class timeStampeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ## Permettre de rendre une class abstraite donc ne peut pas etre hériter !
    class Meta:
        abstract = True

    
class Patient(AbstractBaseUser):
    email=models.EmailField(max_length=254, unique=True)
    prenom =models.CharField(max_length=40)
    nom =models.CharField(max_length=40)
    adress =models.CharField(max_length=100)
    university =models.CharField(max_length=100)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=['email','prenom','nom',"university"]
    
    def __str__(self):
        return self.email
    
    def get_patient(self):
        return self.prenom + ' '
    
    
class Clinicien(AbstractBaseUser):
    email=models.EmailField(max_length=254, unique=True)
    prenom =models.CharField(max_length=40)
    nom =models.CharField(max_length=40)
    adress =models.CharField(max_length=100)
    responsable =models.ForeignKey('self', on_delete=models.CASCADE)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=['email','prenom','nom']

    

class Journal(timeStampeModel):
    id_patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    temps = models.PositiveSmallIntegerField()