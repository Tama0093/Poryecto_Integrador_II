# inventario/context_processors.py
def role_context(request):
    """
    Inyecta el rol del usuario autenticado en el contexto de plantillas.
    Uso en templates: {{ role }}
    """
    role = None
    if request.user.is_authenticated:
        perfil = getattr(request.user, 'perfil', None)
        role = getattr(perfil, 'rol', None)
    return {'role': role}
