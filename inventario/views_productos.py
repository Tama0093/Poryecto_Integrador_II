# inventario/views_productos.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

from .models import Producto
from .forms import ProductoForm
from .permissions import role_and_sucursal

ALLOWED_ROLES_FOR_EDIT = {'Administrador', 'Subadministrador'}  # ← aquí decides quién edita


class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'inventario/producto_list.html'
    context_object_name = 'productos'


class RoleRequiredMixin(LoginRequiredMixin):
    """Bloquea la vista si el rol del usuario no está permitido."""
    allowed_roles = ALLOWED_ROLES_FOR_EDIT

    def dispatch(self, request, *args, **kwargs):
        rol = user_role(request.user)
        if rol not in self.allowed_roles:
            raise PermissionDenied("No tienes permisos para esta acción.")
        return super().dispatch(request, *args, **kwargs)


class ProductoCreateView(RoleRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto_list')


class ProductoUpdateView(RoleRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto_list')


class ProductoDeleteView(RoleRequiredMixin, DeleteView):
    model = Producto
    template_name = 'inventario/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')
