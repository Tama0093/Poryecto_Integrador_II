# inventario/models.py
from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Sucursal(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    ROLES = [
        ('Administrador', 'Administrador'),
        ('Subadministrador', 'Subadministrador'),
        ('Cajero', 'Cajero'),
        ('Supervisión', 'Supervisión'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES, default='Cajero')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.rol})"


class Caja(models.Model):
    ESTADOS = (
        ('ABIERTA', 'ABIERTA'),
        ('CERRADA', 'CERRADA'),
    )

    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='cajas')
    # ✅ Editable, con valor por defecto (no uses auto_now_add si quieres editarla en el form)
    fecha = models.DateField(default=date.today)

    apertura_monto = models.DecimalField(max_digits=12, decimal_places=2)
    cierre_monto = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='ABIERTA')
    apertura_usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='cajas_abiertas')
    cierre_usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='cajas_cerradas', null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sucursal', 'fecha', 'estado')

    def __str__(self):
        return f"Caja {self.sucursal} - {self.fecha} ({self.estado})"


class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='productos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name='ventas')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta {self.producto} x{self.cantidad}"
