# Generated by Django 4.1.6 on 2023-03-10 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_skill_profile_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]