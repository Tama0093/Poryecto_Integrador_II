# inventario/forms.py
from django import forms
from .models import Producto
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
            if rol == 'Administrador':
                # Admin ve todas las sucursales
                pass
            else:
                # Limitar la sucursal a las permitidas
                self.fields['sucursal'].queryset = sucursales_qs
