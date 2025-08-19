# inventario/permissions.py
from .models import Sucursal

def user_role(user):
    """
    Retorna el rol del usuario según su Perfil, o None si no tiene perfil.
    """
    perfil = getattr(user, 'perfil', None)
    return getattr(perfil, 'rol', None) if perfil else None


def role_and_sucursales(user):
    """
    Retorna (rol, lista_de_sucursales_permitidas) para el usuario.

    - Administrador / Subadministrador: acceso a TODAS las sucursales.
    - Cajero / Supervisión: solo a su sucursal asignada (si existe).
    - Sin perfil: (None, [])
    """
    perfil = getattr(user, 'perfil', None)
    if not perfil:
        return None, []

    if perfil.rol in ['Administrador', 'Subadministrador']:
        return perfil.rol, list(Sucursal.objects.all())
    elif perfil.sucursal:
        return perfil.rol, [perfil.sucursal]
    else:
        return perfil.rol, []


def role_and_sucursal(user, sucursal_id):
    """
    True si el usuario puede operar sobre la sucursal indicada (por id).
    Implementado sobre role_and_sucursales().
    """
    rol, sucursales = role_and_sucursales(user)
    return any(s.id == sucursal_id for s in sucursales)
