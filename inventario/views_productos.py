# inventario/views_productos.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Q

from .forms import ProductoForm
from .models import Producto
from .permissions import role_and_sucursales, user_role


ALLOWED_ROLES_FOR_EDIT = {'Administrador', 'Subadministrador'}


class ProductoBase(LoginRequiredMixin):
    """Utilidades comunes para vistas de productos."""

    def get_rol_y_sucursales(self):
        return role_and_sucursales(self.request.user)

    def filtrar_por_permiso(self, qs):
        rol, sucursales = self.get_rol_y_sucursales()
        if rol in ALLOWED_ROLES_FOR_EDIT:
            return qs
        return qs.filter(sucursal__in=sucursales)

    def check_permiso_edicion(self):
        if user_role(self.request.user) not in ALLOWED_ROLES_FOR_EDIT:
            raise PermissionDenied("No tienes permiso para crear/editar productos.")


class ProductoListView(ProductoBase, ListView):
    model = Producto
    template_name = 'inventario/producto_list.html'
    context_object_name = 'productos'
    paginate_by = 20

    def get_queryset(self):
        qs = Producto.objects.select_related('sucursal').order_by('-fecha_creacion', 'nombre')
        qs = self.filtrar_por_permiso(qs)

        # Búsqueda básica ?q=texto
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) |
                Q(descripcion__icontains=q) |
                Q(sucursal__nombre__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class ProductoCreateView(ProductoBase, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto_list')

    def dispatch(self, request, *args, **kwargs):
        self.check_permiso_edicion()
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Producto creado correctamente.")
        return super().form_valid(form)


class ProductoUpdateView(ProductoBase, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto_list')

    def dispatch(self, request, *args, **kwargs):
        self.check_permiso_edicion()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = Producto.objects.all()
        return self.filtrar_por_permiso(qs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado correctamente.")
        return super().form_valid(form)


class ProductoDeleteView(ProductoBase, DeleteView):
    model = Producto
    template_name = 'inventario/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')

    def dispatch(self, request, *args, **kwargs):
        self.check_permiso_edicion()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = Producto.objects.all()
        return self.filtrar_por_permiso(qs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Producto eliminado correctamente.")
        return super().delete(request, *args, **kwargs)
