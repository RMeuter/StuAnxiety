from django.db import models

# Create your models here.
class timeStampeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ## Permettre de rendre une class abstraite donc ne peut pas etre hériter !
    class Meta:
        abstract = True

class Module (timeStampeModel):
    nom =   models.CharField(max_length=50)

class Section(timeStampeModel):
    ordre = models.FloatField()
    titre = models.CharField(max_length=254)
    text = models.TextField()
    image = models.ImageField()
    module = models.ForeignKey('Module', on_delete=models.CASCADE)
    
    REQUIRED_FIELD=["ordre", "module"]

#-------------------------------------- Questionnaire------------------------------------------------------------

class Questionnaire(models.Model):
    nom =   models.CharField(max_length=150)

class Question(models.Model):
    question =   models.CharField(max_length=254)
    questionnaire  = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    
class Response(models.Model):
    reponse =   models.CharField(max_length=254)
    question  = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    
    