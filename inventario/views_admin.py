# inventario/views_admin.py
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms_admin import UsuarioForm, PerfilForm, SucursalForm
from .models import Perfil, Sucursal


# ======== Helpers ========

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restringe el acceso a Administrador/Subadministrador."""
    def test_func(self):
        try:
            return self.request.user.perfil.rol in ['Administrador', 'Subadministrador']
        except Exception:
            return False

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos para acceder a esta sección.")
        return redirect('home')


# ======== Sucursales ========

class SucursalListView(AdminRequiredMixin, ListView):
    model = Sucursal
    template_name = 'sucursales/sucursal_list.html'
    context_object_name = 'sucursales'
    paginate_by = 20


class SucursalCreateView(AdminRequiredMixin, CreateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'sucursales/crear_sucursal.html'
    success_url = reverse_lazy('sucursal_list')

    def form_valid(self, form):
        messages.success(self.request, "Sucursal creada correctamente.")
        return super().form_valid(form)


class SucursalUpdateView(AdminRequiredMixin, UpdateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'sucursales/crear_sucursal.html'  # reusar la misma plantilla
    success_url = reverse_lazy('sucursal_list')

    def form_valid(self, form):
        messages.success(self.request, "Sucursal actualizada correctamente.")
        return super().form_valid(form)


class SucursalDeleteView(AdminRequiredMixin, DeleteView):
    model = Sucursal
    template_name = 'sucursales/sucursal_confirm_delete.html'
    success_url = reverse_lazy('sucursal_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Sucursal eliminada.")
        return super().delete(request, *args, **kwargs)


# ======== Usuarios (User + Perfil) ========

class UsuarioListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 20

    def get_queryset(self):
        # Traer también su perfil si existe
        return User.objects.select_related('perfil').order_by('username')


class UsuarioCreateView(AdminRequiredMixin, View):
    """
    Crea un User (con UserCreationForm) y su Perfil (PerfilForm).
    """
    template_name = 'usuarios/crear_usuario.html'

    def get(self, request):
        return render(request, self.template_name, {
            'u_form': UserCreationForm(),
            'p_form': PerfilForm()
        })

    def post(self, request):
        u_form = UserCreationForm(request.POST)
        p_form = PerfilForm(request.POST)

        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()  # set_password ya lo maneja UserCreationForm
            perfil = p_form.save(commit=False)
            perfil.user = user
            perfil.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect('usuario_list')

        messages.error(request, "Revisa los errores del formulario.")
        return render(request, self.template_name, {'u_form': u_form, 'p_form': p_form})


class UsuarioUpdateView(AdminRequiredMixin, View):
    """
    Edita un User (con UsuarioForm) y su Perfil (PerfilForm).
    Si recibes 'password' en el POST y no está vacío, se actualiza.
    """
    template_name = 'usuarios/editar_usuario.html'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        perfil = getattr(user, 'perfil', None)
        return render(request, self.template_name, {
            'user_obj': user,
            'user_form': UsuarioForm(instance=user),
            'perfil_form': PerfilForm(instance=perfil),
        })

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        perfil = getattr(user, 'perfil', None)

        user_form = UsuarioForm(request.POST, instance=user)
        perfil_form = PerfilForm(request.POST, instance=perfil)

        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save(commit=False)
            # Cambiar contraseña si viene
            new_pass = request.POST.get('password', '').strip()
            if new_pass:
                user.set_password(new_pass)
            user.save()

            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()

            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('usuario_list')

        messages.error(request, "Revisa los errores del formulario.")
        return render(request, self.template_name, {
            'user_obj': user,
            'user_form': user_form,
            'perfil_form': perfil_form
        })


class UsuarioDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Usuario eliminado.")
        return super().delete(request, *args, **kwargs)
