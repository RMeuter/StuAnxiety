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
    class Meta:
        verbose_name="Module"
        ordering=["created_at"]
        
    def __str__(self):
        return self.nom
    
class Section(timeStampeModel):
    titre = models.CharField(max_length=250)
    ordre = models.FloatField()
    text = models.TextField()
    image = models.ImageField()
    module = models.ForeignKey('Module', on_delete=models.CASCADE)
    class Meta:
        verbose_name="Section"
        ordering=["created_at", "ordre"]
        
    def __str__(self):
        return self.titre
        

#-------------------------------------- Questionnaire------------------------------------------------------------
        
class Questionnaire(timeStampeModel):
    nom = models.CharField(max_length=150)
    class Meta:
        verbose_name="Questionnaire"
        ordering=["created_at"]
    def __str__(self):
        return self.nom
class Question(models.Model):
    question =   models.CharField(max_length=250)
    questionnaire  = models.ForeignKey('Questionnaire', on_delete=models.CASCADE)
    def __str__(self):
        return self.question
        
class Response(models.Model):
    reponse =   models.CharField(max_length=250)
    question  = models.ForeignKey('Question', on_delete=models.CASCADE)
    def __str__(self):
        return self.reponse
"""
"""
    
    