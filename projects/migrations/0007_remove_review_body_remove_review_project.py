# Generated by Django 4.1.6 on 2023-02-14 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_review_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='body',
        ),
        migrations.RemoveField(
            model_name='review',
            name='project',
        ),
    ]
