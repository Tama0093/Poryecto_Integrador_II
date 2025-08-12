from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def asignar_rol_por_defecto(sender, instance, created, **kwargs):
    if created:  # Solo al crear un usuario nuevo
        try:
            grupo = Group.objects.get(name='Cajero')  # Rol por defecto
        except Group.DoesNotExist:
            grupo = None

        if grupo:
            instance.groups.add(grupo)
