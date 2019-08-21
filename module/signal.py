from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
from .models import Ordre, Section, Question, Module
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
    if created:
        mod = Module.objects.get(pk=instance.module.pk)
        mod.nbSection+=1
        mod.save()
        if (instance.SectionType==1 and instance.text==None) or (instance.SectionType==3 and instance.video==None) or (instance.SectionType==2 and instance.question==None):
            if instance.text!=None:
                instance.SectionType=1
                instance.save()
            elif instance.video!=None:
                instance.SectionType=3
                instance.save()
            elif instance.question!=None:
                instance.SectionType=2
                instance.save()
            else:
                instance.delete()

@receiver(pre_save, sender=Section)
def verify_double(sender, instance, *args, **kwargs):
        if Section.objects.filter(module=instance.module).exists():
            instance.ordre = Section.objects.filter(module=instance.module).aggregate(Max('ordre')).ordre +1
                