from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    user = request.user

    # Definir rol y opciones
    if user.groups.filter(name='Administrador').exists():
        role = 'Administrador'
        opciones = [
            {"titulo": "Inventario", "desc": "Registrar y consultar productos."},
            {"titulo": "Caja y Ventas", "desc": "Apertura, ventas y cierre diario."},
            {"titulo": "Reportes", "desc": "Exportar ventas a Excel."}
        ]
    elif user.groups.filter(name='Subadministrador').exists():
        role = 'Subadministrador'
        opciones = [
            {"titulo": "Inventario", "desc": "Registrar y consultar productos."},
            {"titulo": "Caja y Ventas", "desc": "Apertura, ventas y cierre diario."}
        ]
    elif user.groups.filter(name='Cajero').exists():
        role = 'Cajero'
        opciones = [
            {"titulo": "Caja y Ventas", "desc": "Apertura, ventas y cierre diario."}
        ]
    else:
        role = 'Sin rol'
        opciones = []

    return render(request, 'inventario/home.html', {
        'role': role,
        'opciones': opciones
    })
