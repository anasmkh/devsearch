from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User


def userCreate(sender, instance,created,**kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name

        )

def updateUser(sender,instance,created,**kwargs):
    profile = instance
    user = profile.user
    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deletUser(sender,instance,**kwargs):
    user=instance.user
    user.delete()


post_save.connect(userCreate,sender=User)
post_save.connect(updateUser,sender = Profile)
post_delete.connect(deletUser,sender=Profile)