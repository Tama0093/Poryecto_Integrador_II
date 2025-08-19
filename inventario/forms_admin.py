# inventario/forms_admin.py
from django import forms
from django.contrib.auth.models import User
from .models import Perfil, Sucursal


class UsuarioForm(forms.ModelForm):
    """
    Form para EDITAR usuarios (no crea). Permite opcionalmente cambiar la contraseña.
    """
    password = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(render_value=False),
        required=False,
        help_text="Déjalo vacío si no deseas cambiar la contraseña."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'autofocus': True}),
            'email': forms.EmailInput(),
        }


class PerfilForm(forms.ModelForm):
    """
    Form para crear/editar Perfil asociado a un User.
    """
    class Meta:
        model = Perfil
        fields = ['rol', 'sucursal']
        widgets = {
            'rol': forms.Select(),
            'sucursal': forms.Select(),
        }

    def clean(self):
        cleaned = super().clean()
        rol = cleaned.get('rol')
        sucursal = cleaned.get('sucursal')

        # Si el rol NO es admin/subadmin, exigir sucursal
        if rol not in ['Administrador', 'Subadministrador'] and not sucursal:
            self.add_error('sucursal', 'Para este rol debes seleccionar una sucursal.')
        return cleaned


class SucursalForm(forms.ModelForm):
    """
    CRUD de Sucursales.
    """
    class Meta:
        model = Sucursal
        fields = ['nombre', 'direccion', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'autofocus': True}),
            'direccion': forms.TextInput(),
            'telefono': forms.TextInput(),
        }
