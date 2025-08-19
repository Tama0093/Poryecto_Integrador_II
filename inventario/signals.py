# inventario/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Perfil

@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    """
    Crea automáticamente un Perfil cuando se crea un User.
    (Por defecto rol = 'Cajero' y sin sucursal asignada)
    """
    if created:
        Perfil.objects.create(user=instance)
