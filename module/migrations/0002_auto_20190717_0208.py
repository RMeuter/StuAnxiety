# Generated by Django 2.2.1 on 2019-07-17 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='isMultipleRep',
            field=models.BooleanField(choices=[(True, 'Plusieurs choix de réponses possibles'), (False, 'Une seul réponse')], default=False),
        ),
    ]