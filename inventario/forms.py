# inventario/forms.py
from django import forms
from django.utils import timezone
from .models import Producto, Caja, Venta
from .permissions import role_and_sucursales


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'sucursal']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # le pasaremos el user desde la vista
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            rol, sucursales_qs = role_and_sucursales(user)
            if rol != 'Administrador':
                # Limitar la sucursal a las permitidas (Subadmin/Cajero)
                self.fields['sucursal'].queryset = sucursales_qs


class CajaAperturaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ['sucursal', 'apertura_monto', 'fecha']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # fecha por defecto: hoy
        if not self.instance.pk:
            self.fields['fecha'].initial = timezone.now().date()
        # limitar sucursales por rol
        if user and user.is_authenticated:
            rol, sucs = role_and_sucursales(user)
            if rol != 'Administrador':
                self.fields['sucursal'].queryset = sucs


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['producto', 'cantidad']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        caja = kwargs.pop('caja', None)
        super().__init__(*args, **kwargs)
        # limitar productos por sucursal de la caja
        if caja:
            self.fields['producto'].queryset = Producto.objects.filter(sucursal=caja.sucursal)
        # cantidad por defecto 1
        if not self.instance.pk:
            self.fields['cantidad'].initial = 1

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is None or cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que 0.")
        return cantidad
