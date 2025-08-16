# inventario/forms.py
from django import forms
from django.utils import timezone
from .models import Producto, Caja, Venta
from .permissions import role_and_sucursal


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'sucursal']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # le pasaremos el user desde la vista
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            rol, sucursales_qs = role_and_sucursal(user)  # 🛠️ corrección aquí
            if rol != 'Administrador':
                # Limitar la sucursal a la asignada (Subadmin/Cajero/Supervisión)
                self.fields['sucursal'].queryset = sucursales_qs


class CajaAperturaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ['sucursal', 'apertura_monto', 'fecha']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['fecha'].initial = timezone.now().date()
        if user and user.is_authenticated:
            rol, sucs = role_and_sucursal(user)
            if rol != 'Administrador':
                self.fields['sucursal'].queryset = sucs


class VentaForm(forms.ModelForm):
    """
    Muestra productos de la sucursal asignada al usuario,
    pero valida que el producto pertenezca a la sucursal de la caja actual.
    """
    class Meta:
        model = Venta
        fields = ['producto', 'cantidad']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.caja = kwargs.pop('caja', None)
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields['cantidad'].initial = 1

        if self.user and self.user.is_authenticated:
            rol, sucs = role_and_sucursal(self.user)
            if rol == 'Administrador':
                self.fields['producto'].queryset = Producto.objects.all()
            else:
                self.fields['producto'].queryset = Producto.objects.filter(sucursal__in=sucs)

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is None or cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que 0.")
        return cantidad

    def clean(self):
        cleaned = super().clean()
        producto = cleaned.get('producto')

        if self.caja and producto:
            if producto.sucursal_id != self.caja.sucursal_id:
                raise forms.ValidationError(
                    "El producto seleccionado pertenece a la sucursal "
                    f"'{producto.sucursal.nombre}', pero la caja actual es de "
                    f"'{self.caja.sucursal.nombre}'. "
                    "Abre o usa la caja de la sucursal correcta para registrar esta venta."
                )
        return cleaned
