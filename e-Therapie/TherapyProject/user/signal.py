#Model et attribut de signal !
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Patient, Clinicien, Population, enAttente
from module.models import Sequence
from django.contrib.auth.models import User, Group

#Ajouter des permissions  pour les groupes
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# checker la permission d'une séquence
from django.contrib.auth.decorators import permission_required
"""
S'entrainer : https://openclassrooms.com/fr/courses/1871271-developpez-votre-site-web-avec-le-framework-django/1873451-les-signaux-et-middlewares
"""

########################################## Affectation auto sequence pour groupe 2 ##################################
@receiver(post_save, sender=Patient)
def Affecte_sequence(sender,created, instance, **kwargs):
    print("fonction affect sequence")
    if instance.groupePatients != None :
        if instance.groupePatients.categorie == 2 and instance.sequence == None:
            print("passe 1")
            seq = Sequence.objects.create(nom="Sequence de {0} {1}".format(instance.user.first_name,instance.user.last_name))
            print(seq)
            instance.sequence = seq
            instance.save()
        elif instance.groupePatients.categorie != 2 and instance.sequence != None :
            print("passe 2")
            instance.sequence.delete()
            
########################################## Affectation de permission ##################################
    
@receiver(post_save, sender=Population)
def Affectation_Permission_Groupe(sender,created, instance, **kwargs):
    """
    On permet les différent parcours selon les catégories de groupe
    https://stackoverflow.com/questions/10131271/invalid-literal-error-when-adding-a-user-permission-to-a-django-user-object
    https://www.vinta.com.br/blog/2016/controlling-access-a-django-permission-apps-comparison/
    
    https://cheat.readthedocs.io/en/latest/django/permissions.html
    
    Faire attention au répetion permission car elle sont écraser dans le else!
    
    ###########Attention à la mise en cache !##############
    
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

"""
@receiver(pre_save, sender=enAttente)
def verifie_double_et_impossibilite_enAttente(sender, instance, *args, **kwargs):
    if enAttente.objects.filter(patient=instance.patient, module=instance.module, forClinicien=False).exists():
        enAttente.objects.filter(patient=instance.patient, module=instance.module, forClinicien=False).delete()
"""
############################### Integration de groupe pour les permission#####################################

@receiver(post_save, sender=Patient)
def integre_group(sender,created, instance, *args, **kwargs):
    
    user=User.objects.get(pk=instance.user.pk)
    user.groups.clear()
    gp =Group.objects.get(pk=instance.groupePatients.groupe.pk)
    user.groups.add(gp)

@receiver(post_save, sender=Clinicien)
def integre_group(sender,created, instance, *args, **kwargs):
    
    user=User.objects.get(pk=instance.user.pk)
    user.groups.clear()
    gp =Group.objects.get(pk=instance.equipe.groupe.pk)
    user.groups.add(gp)
