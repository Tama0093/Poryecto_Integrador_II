from .models import Sucursal

def role_and_sucursal(user, sucursal_id):
    """
    Verifica si el usuario tiene permiso para operar sobre una sucursal específica.
    Aplica a roles que deben estar asociados a una única sucursal (no múltiples).
    """
    perfil = getattr(user, 'perfil', None)
    
    if not perfil:
        return False

    if perfil.rol in ['Administrador', 'Subadministrador', 'Supervisión']:
        return perfil.sucursal and perfil.sucursal.id == sucursal_id

    return False


def role_and_sucursales(user):
    """
    Retorna el rol del usuario y las sucursales a las que tiene acceso.
    """
    perfil = getattr(user, 'perfil', None)
    
    if not perfil:
        return None, []

    if perfil.rol == 'Administrador':
        return 'Administrador', Sucursal.objects.all()
    elif perfil.rol == 'Supervisión':
        return 'Supervisión', Sucursal.objects.all()
    elif hasattr(perfil, 'sucursal'):
        return perfil.rol, [perfil.sucursal]
    else:
        return perfil.rol, []
