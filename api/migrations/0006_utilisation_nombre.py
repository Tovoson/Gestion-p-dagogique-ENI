# Generated by Django 5.1.1 on 2024-11-04 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_materiel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisation',
            name='nombre',
            field=models.CharField(default='0', max_length=10),
        ),
    ]
