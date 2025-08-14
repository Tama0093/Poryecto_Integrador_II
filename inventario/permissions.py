# inventario/permissions.py
from .models import Sucursal

def role_and_sucursales(user):
    """
    Devuelve (rol, queryset_de_sucursales_permitidas)
    - Administrador: todas las sucursales
    - Subadministrador/Cajero: solo sus sucursales del Perfil
    - Sin perfil: queryset vacío
    """
    perfil = getattr(user, 'perfil', None)
    if not perfil:
        return None, Sucursal.objects.none()

    rol = perfil.rol
    if rol == 'Administrador':
        return rol, Sucursal.objects.all()
    return rol, perfil.sucursales.all()
