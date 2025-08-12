from django.db import models
from django.contrib.auth.models import User

class Sucursal(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=250, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        suc = self.sucursal.nombre if self.sucursal else "Sin sucursal"
        return f"{self.user.username} — {suc}"
