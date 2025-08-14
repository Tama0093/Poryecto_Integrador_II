# models.py
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
    ROLES = (
        ('Administrador', 'Administrador'),
        ('Subadministrador', 'Subadministrador'),
        ('Cajero', 'Cajero'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    sucursales = models.ManyToManyField(Sucursal, blank=True, related_name='perfiles')  # 👈 M2M
    rol = models.CharField(max_length=20, choices=ROLES, default='Cajero')

    def __str__(self):
        sucs = ", ".join(s.nombre for s in self.sucursales.all()) or "Sin sucursales"
        return f"{self.user.username} — {self.rol} — {sucs}"



class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='productos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.sucursal.nombre})"
