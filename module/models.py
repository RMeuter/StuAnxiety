from django.db import models
from django.core.validators import MaxValueValidator
from ckeditor_uploader.fields import RichTextUploadingField



#-------------------------------------- Question------------------------------------------------------------
    
class Question(models.Model):
    """
    On choisit un type d'input qui par le questionnaire sera automatiquement mis pour teste
    """
    
    
    INPUT_TYPE = [(1, 'Selectionner une réponse ou plusieurs réponses'), (2, 'Bouton radio'),(3, 'Case à cocher (réponse multiple)'),(4, "Reponse texte libre"),(5, "Reponse gradué libre")]
    inputType = models.IntegerField(choices=INPUT_TYPE)
    MULTIPLE_INPUT = [(True, 'Plusieurs choix de réponses possibles'), (False, 'Une seul réponse')]
    isMultipleRep = models.BooleanField(default=False, choices=MULTIPLE_INPUT)
    isRequired = models.BooleanField(default=False)
    question =   models.CharField(max_length=250)
    consigne =   models.CharField(max_length=250, null=True, blank=True)
    intervaleGraduerInput = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)]) # si différent de 0 c'est un input de type gradué
    
    
    def __str__(self):
        return "{0}".format(self.question)
        
        
class Reponse(models.Model):
    """
    Reponse possible si ce sont des choix mais l'intégration des reponses choisit par un patient est resultat. 
    """
    reponse =   models.CharField(max_length=250)
    question  = models.ForeignKey(Question, on_delete=models.CASCADE)
    class Meta:
        ordering=["question"]
    def __str__(self):
        return "{0} {1}".format(self.reponse,self.pk )

#-------------------------------------- Module------------------------------------------------------------

class Module (models.Model):
    """
    Un module est soit un questionnaire par son booléan et donc sera affecter de façon différente qu'un module d'apprentissage normal, il est unifier pour plus de facilité et de ompréhension lors de la création des séquences
    """
    nom =   models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    image = models.ImageField(upload_to="imageModule/", blank=True)
    #Pour opitimiser les requet et savoir si le module peut etre visible
    nbSection=models.PositiveSmallIntegerField(default=0)
    isVisible=models.BooleanField(default=False)
    isQuestionnaireOnly=models.BooleanField(default=False)
    isJournal=models.BooleanField(default=False)
    questionnaireDependant = models.ForeignKey("self", on_delete=models.SET_NULL,null=True, blank=True,limit_choices_to={'isQuestionnaireOnly': True})
    class Meta:
        ordering=["isQuestionnaireOnly", "isVisible",]
    def __str__(self):
        return self.nom


class Section(models.Model):
    """
    Il y a trois choix possible mais pas en meme temps, soit une vidéo, soit un pdf, soit une question
    """
       
    ####################### Base de la section
    titre = models.CharField(max_length=250)
    ordre = models.PositiveSmallIntegerField(default=1)
    module = models.ForeignKey('Module', on_delete=models.CASCADE)
    SECTION_TYPE = [(1, 'Texte et images'), (2, 'Question'),(3, 'Vidéo')]
    SectionType = models.IntegerField(choices=SECTION_TYPE)
    ####################### Intégration de la section
    question = models.ForeignKey('Question', on_delete=models.SET_NULL,null=True, blank=True)
    text = RichTextUploadingField(null=True, blank=True)
    video = models.CharField(max_length=50,null=True, blank=True)
    class Meta:
        ordering=["module","ordre"]
    def __str__(self):
        return "{0} : {1} {2}".format(self.module, self.titre,self.ordre )
    def move_to_good_type (self):
        """
        Donne le type de section correspondante au type remplie si oublie ou erreur. Si rien rempli elle est supprimer.
        :return:
        """
        if (self.SectionType == 1 and self.text == None) or (
                self.SectionType == 3 and self.video == None) or (
                self.SectionType == 2 and self.question == None):
            if self.text != None:
                self.SectionType = 1
                self.save()
            elif self.video != None:
                self.SectionType = 3
                self.save()
            elif self.question != None:
                self.SectionType = 2
                self.save()
            else:
                self.delete()



#-------------------------------------- Sequence ------------------------------------------------------------

class Sequence(models.Model):
    """
    Une sequence est une liste de module qui s'enchaineront selon un ordre précis pour le patient, permet des tests expérimentaux des différents parcours.
    """
    nom= models.CharField(max_length=250)
    possede = models.ManyToManyField(Module, through="Ordre", blank=True)
    nbModule=models.PositiveSmallIntegerField(default=0)
    def __str__(self):
        return self.nom
    
    class Meta:
        permissions =(
        ("Sequence_Groupal", "Affecter une sequence de façon groupale"),
        ("Sequence_Individuel", "Affecter une sequence de façon individuelle")
        )
        
class Ordre(models.Model):
    """
    Un ordre est un modules possitionner à un rang précis pour permettre l'enchainnement de module dans un ordre au sein d'une sequence
    """
    sequence = models.ForeignKey(Sequence,on_delete=models.CASCADE)
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    ordre = models.PositiveSmallIntegerField()
    class Meta:
        ordering=["sequence","ordre"]
    def __str__(self):
        return "{0} : {1} comme rang {2}".format(self.sequence.nom, self.module.nom, self.ordre)    
 
