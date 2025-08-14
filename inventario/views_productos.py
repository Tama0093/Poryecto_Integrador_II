# inventario/views_productos.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

from .models import Producto
from .forms import ProductoForm
from .permissions import role_and_sucursales

class ProductoQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        rol, sucursales_qs = role_and_sucursales(self.request.user)
        if rol == 'Administrador':
            return Producto.objects.select_related('sucursal')
        return Producto.objects.select_related('sucursal').filter(sucursal__in=sucursales_qs)

class ProductoListView(ProductoQuerysetMixin, ListView):
    model = Producto
    template_name = 'inventario/producto_list.html'
    context_object_name = 'productos'

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # para limitar sucursales en el form
        return kwargs

    def form_valid(self, form):
        # Seguridad extra: validar que la sucursal elegida esté permitida
        rol, sucursales_qs = role_and_sucursales(self.request.user)
        if rol != 'Administrador' and form.cleaned_data['sucursal'] not in sucursales_qs:
            raise PermissionDenied("No puedes crear productos en esa sucursal.")
        return super().form_valid(form)

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto_list')

    def get_queryset(self):
        # Solo puede editar productos dentro de sus sucursales
        rol, sucursales_qs = role_and_sucursales(self.request.user)
        if rol == 'Administrador':
            return Producto.objects.all()
        return Producto.objects.filter(sucursal__in=sucursales_qs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'inventario/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')

    def get_queryset(self):
        rol, sucursales_qs = role_and_sucursales(self.request.user)
        if rol == 'Administrador':
            return Producto.objects.all()
        return Producto.objects.filter(sucursal__in=sucursales_qs)
