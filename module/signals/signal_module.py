from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
from module.models import Section, Module
from django.db.models import Max


@receiver(pre_delete, sender=Section)
def delete_ordre_pre_delete_section(sender, instance, *args, **kwargs):
    """
    Redéfinition de l'ordre dans un module à chaque suppression d'une section
    """
    if instance.ordre:
        depart = instance.ordre
        sections = Section.objects.filter(ordre__gt=depart, module=instance.module).order_by('ordre')
        for sec in sections:
            sec.ordre =depart
            depart+=1
            sec.save()
        mod = Module.objects.get(pk=instance.module.pk)
        mod.nbSection=depart-1
        mod.save()

@receiver(post_save, sender=Section)
def add_nb_section_and_verify_typeSection(sender, instance, created, *args, **kwargs):
    """
    :param instance: Ma section apres sauvegarde
    :param created:  Si ma section à été sauvegarder
    A chaque création d'une section le parametre du module nbsection augmente de 1
    A chaque modification de section on réordonne de 1 à len(listSec) les sections du module concerné
    Le programme verifie si le type de section correspond bien au champs remplit
    """
    instance.move_to_good_type()
    if created:
        mod = Module.objects.get(pk=instance.module.pk)
        mod.nbSection+=1
        mod.save()
    else :
        cpt=1
        listSection=Section.objects.filter(module=instance.module).order_by("ordre")
        for sec in listSection:
            if instance.ordre != cpt:
                if sec.ordre < cpt:
                    sec.ordre=cpt
                cpt+=1

@receiver(pre_save, sender=Section)
def verify_double(sender, instance, *args, **kwargs):
    """
    :param instance: Ma section
    :return: L'odre +1 de la section possédant l'ordre maximal
    """
    if Section.objects.filter(module=instance.module).exists():
        val= Section.objects.filter(module=instance.module).aggregate(Max('ordre'))["ordre__max"]
        instance.ordre =  val +1