# Generated by Django 4.1.6 on 2023-03-10 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_skill_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
