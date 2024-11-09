from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profesor

@receiver(post_save, sender=User)
def crear_perfil_profesor(sender, instance, created, **kwargs):
    if created:
        Profesor.objects.create(user=instance, nombre=instance.username)

@receiver(post_save, sender=User)
def guardar_perfil_profesor(sender, instance, **kwargs):
    if hasattr(instance, 'profesor'):
        instance.profesor.save()
