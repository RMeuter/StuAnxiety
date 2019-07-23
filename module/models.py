from django.db import models
from django.core.validators import MaxValueValidator
from ckeditor_uploader.fields import RichTextUploadingField


#-------------------------------------- Question------------------------------------------------------------
    
class Question(models.Model):
   
    question =   models.CharField(max_length=250)
    consigne =   models.CharField(max_length=250, null=True, blank=True)
    intervaleGraduerInput = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)]) # si différent de 0 c'est un input de type gradué
    
    INPUT_TYPE = [(1, 'Selectionner une réponse ou plusieurs réponses'), (2, 'Bouton radio'),(3, 'Case à cocher (réponse multiple)'),(4, "Reponse texte libre"),(5, "Reponse gradué libre")]
    inputType = models.IntegerField(choices=INPUT_TYPE)
    MULTIPLE_INPUT = [(True, 'Plusieurs choix de réponses possibles'), (False, 'Une seul réponse')]
    isMultipleRep = models.BooleanField(default=False, choices=MULTIPLE_INPUT)
    
    def __str__(self):
        return "{0}".format(self.question)
        
        
class Reponse(models.Model):
    reponse =   models.CharField(max_length=250)
    question  = models.ForeignKey(Question, on_delete=models.CASCADE)
    class Meta:
        ordering=["question"]
    def __str__(self):
        return "{0} {1}".format(self.reponse,self.pk )

#-------------------------------------- Module------------------------------------------------------------

class Module (models.Model):
    nom =   models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    image = models.ImageField(upload_to="imageModule/", blank=True)
    #Pour opitimiser les requet et savoir si le module peut etre visible
    nbSection=models.PositiveSmallIntegerField(default=0)
    isVisible=models.BooleanField(default=False)
    isQuestionnaireOnly=models.BooleanField(default=False)
    isJournal=models.BooleanField(default=False)
    questionnaireDependant = models.ForeignKey("self", on_delete=models.SET_NULL,null=True, blank=True) 
    def __str__(self):
        return self.nom


class Section(models.Model):
    """
    Il y a trois choix possible mais pas en meme temps, soit une vidéo, soit un pdf, soit une question
    """
    ####################### Base de la section
    titre = models.CharField(max_length=250)
    ordre = models.PositiveSmallIntegerField()
    SECTION_TYPE = [(1, 'Texte et images'), (2, 'Question'),(3, 'Vidéo')]
    SectionType = models.IntegerField(choices=SECTION_TYPE)
    ####################### Intégration de la section
    question = models.ForeignKey('Question', on_delete=models.SET_NULL,null=True, blank=True)
    module = models.ForeignKey('Module', on_delete=models.CASCADE)
    text = RichTextUploadingField(null=True, blank=True)
    video = models.CharField(max_length=50,null=True, blank=True)
    class Meta:
        ordering=["module","ordre"]
    def __str__(self):
        return "{0} : {1} {2}".format(self.module, self.titre,self.ordre )

#-------------------------------------- Sequence ------------------------------------------------------------

class Sequence(models.Model):
    """
    Une sequence est une liste de module qui s'enchaineront selon un ordre précis pour le patient, permet des tests expérimentaux des différents parcours.
    """
    nom= models.CharField(max_length=250)
    possede = models.ManyToManyField(Module, through="ordre", blank=True)
    nbModule=models.PositiveSmallIntegerField(default=0)
    def __str__(self):
        return self.nom
    
    class Meta:
        permissions =(
        ("Sequence_Groupal", "Affecter une sequence de façon groupale"),
        ("Sequence_Individuel", "Affecter une sequence de façon individuelle")
        )
        
class Ordre(models.Model):
    sequence = models.ForeignKey(Sequence,on_delete=models.CASCADE)
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    ordre = models.PositiveSmallIntegerField()
    class Meta:
        ordering=["sequence","ordre"]
    def __str__(self):
        return "{0} : {1} comme rang {2}".format(self.sequence.nom, self.module.nom, self.ordre)    
 
