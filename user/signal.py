#Model et attribut de signal !
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Patient, Clinicien, Population
from module.models import Sequence
from django.contrib.auth.models import User, Group

#Ajouter des permissions  pour les groupes
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

########################################## Affectation auto sequence pour groupe 2 ##################################
@receiver(post_save, sender=Patient)
def Affecte_sequence(sender,created, instance, **kwargs):
    """
    La focntion affecte une séquence de module vide si le patient est en groupe de catégorie 2. S'il en possède une et qu'il
    n'est pas en 2, elle est automatique détruite.
    """
    print("fonction affect sequence")
    if instance.groupePatients != None :
        if instance.groupePatients.categorie == 2 and instance.sequence == None:
            seq = Sequence.objects.create(nom="Sequence de {0} {1}".format(instance.user.first_name,instance.user.last_name))
            instance.sequence = seq
            instance.save()
        elif instance.groupePatients.categorie != 2 and instance.sequence != None :
            instance.sequence.delete()
            
########################################## Affectation de permission ##################################
    
@receiver(post_save, sender=Population)
def Affectation_Permission_Groupe(sender,created, instance, **kwargs):
    """
    Si le groupe ne vient pas d'etre crée on écrase ces permissions
    Ensuite la fonction affecte les permissions ciblés selon sa catégorie

    """
    print("fonction affect groupe et pop")
    if not created :
        # Une fois qu'on modifie un groupe on enlève toute ces permissions et on le recré selon la categorie
        instance.groupe.permissions.clear()
    content_type = ContentType.objects.get_for_model(Population)

    if instance.categorie == 1:
        permission = Permission.objects.get(content_type=content_type, codename='parcours_Clinicien')
        instance.groupe.permissions.add(permission)
    elif instance.categorie == 5:
        permission = Permission.objects.get(content_type=content_type, codename='parcours_Patient_Non_Suivie')
        instance.groupe.permissions.add(permission)
    else :
        permission = Permission.objects.get(content_type=content_type, codename='parcours_Patient_Suivie')
        instance.groupe.permissions.add(permission)

        content_type = ContentType.objects.get_for_model(Sequence)
        if instance.categorie == 2:
            permission = Permission.objects.get(content_type=content_type, codename='Sequence_Individuel')
            instance.groupe.permissions.add(permission)
        elif instance.categorie == 3:
            permission = Permission.objects.get(content_type=content_type, codename='Sequence_Groupal')
            instance.groupe.permissions.add(permission)

############################### Integration de groupe pour les permission#####################################

@receiver(post_save, sender=Patient)
def integre_group(sender,created, instance, *args, **kwargs):
    """
     La fonction efface tous les liens avec les autre groupes pour affecter uniquement le lien appartenant au groupe affecter
    """
    user=User.objects.get(pk=instance.user.pk)
    user.groups.clear()
    gp =Group.objects.get(pk=instance.groupePatients.groupe.pk)
    user.groups.add(gp)

@receiver(post_save, sender=Clinicien)
def integre_group(sender,created, instance, *args, **kwargs):
    """
    La fonction efface tous les liens avec les autre groupes pour affecter uniquement le lien appartenant au groupe affecter
    """
    user=User.objects.get(pk=instance.user.pk)
    user.groups.clear()
    gp =Group.objects.get(pk=instance.equipe.groupe.pk)
    user.groups.add(gp)
