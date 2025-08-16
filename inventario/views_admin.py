# inventario/views_admin.py
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .forms_admin import UsuarioForm, PerfilForm, SucursalForm
from .models import Perfil

def es_admin(user):
    try:
        return user.perfil.rol in ['Administrador', 'Subadministrador']
    except:
        return False

@login_required
@user_passes_test(es_admin)
def crear_usuario(request):
    if request.method == 'POST':
        u_form = UsuarioForm(request.POST)
        p_form = PerfilForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save(commit=False)
            user.set_password(u_form.cleaned_data['password'])
            user.save()
            perfil = p_form.save(commit=False)
            perfil.user = user
            perfil.save()
            return redirect('home')
    else:
        u_form = UsuarioForm()
        p_form = PerfilForm()
    return render(request, 'adminweb/crear_usuario.html', {'u_form': u_form, 'p_form': p_form})

@login_required
@user_passes_test(es_admin)
def crear_sucursal(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SucursalForm()
    return render(request, 'adminweb/crear_sucursal.html', {'form': form})


    from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Perfil, Sucursal
from .forms_admin import UsuarioForm, PerfilForm, SucursalForm

# Vista para crear usuario + perfil
def crear_usuario(request):
    if request.method == 'POST':
        user_form = UsuarioForm(request.POST)
        perfil_form = PerfilForm(request.POST)
        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save()
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()
            return redirect('home')
    else:
        user_form = UsuarioForm()
        perfil_form = PerfilForm()
    return render(request, 'usuarios/crear_usuario.html', {
        'user_form': user_form,
        'perfil_form': perfil_form
    })

# Vista para crear sucursal
def crear_sucursal(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SucursalForm()
    return render(request, 'usuarios/crear_sucursal.html', {'form': form})

