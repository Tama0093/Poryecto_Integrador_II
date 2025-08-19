# inventario/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Caja, Venta, Producto, Sucursal
from .permissions import role_and_sucursales


class CajaAperturaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ['sucursal', 'fecha', 'apertura_monto']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            rol, sucursales = role_and_sucursales(self.user)
            if rol in ['Administrador', 'Subadministrador']:
                self.fields['sucursal'].queryset = Sucursal.objects.all()
            else:
                self.fields['sucursal'].queryset = Sucursal.objects.filter(
                    id__in=[s.id for s in sucursales]
                )
        else:
            self.fields['sucursal'].queryset = Sucursal.objects.none()

        self.fields['apertura_monto'].min_value = 0

    def clean(self):
        cleaned = super().clean()
        sucursal = cleaned.get('sucursal')
        fecha = cleaned.get('fecha')
        if sucursal and fecha:
            existe_abierta = Caja.objects.filter(
                sucursal=sucursal, fecha=fecha, estado='ABIERTA'
            ).exists()
            if existe_abierta:
                raise ValidationError(
                    "Ya existe una caja ABIERTA para esa sucursal y fecha."
                )
        return cleaned


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['producto', 'cantidad']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.caja = kwargs.pop('caja', None)
        super().__init__(*args, **kwargs)

        productos_qs = Producto.objects.all()

        # Filtrar productos por rol
        if self.user:
            rol, sucursales = role_and_sucursales(self.user)
            if rol not in ['Administrador', 'Subadministrador']:
                productos_qs = productos_qs.filter(sucursal__in=sucursales)

        # Filtrar por sucursal de la caja activa
        if self.caja:
            productos_qs = productos_qs.filter(sucursal=self.caja.sucursal)

        self.fields['producto'].queryset = productos_qs
        self.fields['cantidad'].min_value = 1

    def clean(self):
        cleaned = super().clean()
        producto = cleaned.get('producto')
        cantidad = cleaned.get('cantidad')

        if producto and cantidad:
            if cantidad <= 0:
                self.add_error('cantidad', 'La cantidad debe ser mayor que 0.')
            if producto.stock < cantidad:
                # Permitimos registrar pero avisamos (la vista muestra mensaje)
                # Si quieres bloquear, descomenta la siguiente línea:
                # self.add_error('cantidad', 'Stock insuficiente para la venta.')
                pass
        return cleaned


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'sucursal']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['precio'].min_value = 0
        self.fields['stock'].min_value = 0

        if user:
            rol, sucursales = role_and_sucursales(user)
            if rol in ['Administrador', 'Subadministrador']:
                self.fields['sucursal'].queryset = Sucursal.objects.all()
            else:
                self.fields['sucursal'].queryset = Sucursal.objects.filter(
                    id__in=[s.id for s in sucursales]
                )
        else:
            self.fields['sucursal'].queryset = Sucursal.objects.none()
