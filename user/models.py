from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class timeStampeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ## Permettre de rendre une class abstraite donc ne peut pas etre hériter !
    class Meta:
        abstract = True



class Patient(timeStampeModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return "Etudiant ".format(self.user.username)

class Journal(timeStampeModel):
    id_patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    temps = models.PositiveSmallIntegerField()
