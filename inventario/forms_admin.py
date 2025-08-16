# inventario/forms_admin.py
from django import forms
from django.contrib.auth.models import User
from .models import Perfil, Sucursal
from django.contrib.auth.forms import UserCreationForm

class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre', 'direccion', 'telefono']

class UsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label='Nombres')
    last_name = forms.CharField(label='Apellidos')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['sucursal', 'rol']
