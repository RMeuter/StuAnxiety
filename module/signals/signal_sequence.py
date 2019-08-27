from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from module.models import Ordre,Sequence


@receiver(pre_delete, sender=Ordre)
def delete_ordre_pre_delete_section(sender, instance, *args, **kwargs):
    """
    Redéfinition de l'ordre dans un module à chaque suppression d'une section
    """
    seq = Sequence.objects.get(pk=instance.module.pk)
    seq.nbModule-=1
    seq.save()

@receiver(post_save, sender=Ordre)
def add_nb_section(sender, instance, created, *args, **kwargs):
    """
    :param instance: Mon ordre apres sauvegarde
    :param created:  Si mon ordre à été sauvegarder
    A chaque création d'un ordre on réordonne de 1 à len(listSec) les sections du module concerné
    """
    if created:
        seq = Sequence.objects.get(pk=instance.module.pk)
        seq.nbModule += 1
        seq.save()