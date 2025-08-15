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


 # ... Sucursal, Perfil, Producto arriba ...

class Caja(models.Model):
    ESTADOS = (('ABIERTA', 'ABIERTA'), ('CERRADA', 'CERRADA'))

    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='cajas')
    fecha = models.DateField()  # 1 caja por día por sucursal
    apertura_monto = models.DecimalField(max_digits=12, decimal_places=2)
    apertura_usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='aperturas_caja')
    cierre_monto = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cierre_usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='cierres_caja')
    estado = models.CharField(max_length=10, choices=ESTADOS, default='ABIERTA')
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sucursal', 'fecha')  # evita dos cajas el mismo día en la misma sucursal

    def __str__(self):
        return f"Caja {self.sucursal.nombre} — {self.fecha} — {self.estado}"

    @property
    def total_ventas(self):
        agg = self.ventas.aggregate(s=models.Sum('total'))
        return agg['s'] or 0


class Venta(models.Model):
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name='ventas')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta {self.producto.nombre} x{self.cantidad} — {self.total}"       
