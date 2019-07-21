from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import Ordre, Section, Question, Module


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
def add_nb_section(sender, instance, created, *args, **kwargs):
    if created:
        mod = Module.objects.get(pk=instance.module.pk)
        mod.nbSection+=1
        mod.save()
        
          
