from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    user = request.user
    if user.groups.filter(name='Administrador').exists():
        role = 'Administrador'
    elif user.groups.filter(name='Subadministrador').exists():
        role = 'Subadministrador'
    elif user.groups.filter(name='Cajero').exists():
        role = 'Cajero'
    else:
        role = 'Sin rol'
    return render(request, 'inventario/home.html', {'role': role})
