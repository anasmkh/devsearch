# Generated by Django 4.1.6 on 2023-02-14 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='titel',
            new_name='title',
        ),
    ]
