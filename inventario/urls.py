# inventario/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views_reportes

from . import views
from .views_productos import (
    ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView
)
from . import views_caja
from . import views_admin

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Autenticación
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    # Productos
    path('productos/', ProductoListView.as_view(), name='producto_list'),
    path('productos/nuevo/', ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/eliminar/', ProductoDeleteView.as_view(), name='producto_delete'),

    # Caja y ventas
    path('caja/', views_caja.caja_estado, name='caja_estado'),
    path('caja/abrir/', views_caja.caja_abrir, name='caja_abrir'),
    path('caja/<int:caja_id>/', views_caja.caja_detalle, name='caja_detalle'),
    path('caja/<int:caja_id>/venta/nueva/', views_caja.venta_nueva, name='venta_nueva'),
    path('caja/<int:caja_id>/cerrar/', views_caja.caja_cerrar, name='caja_cerrar'),

    # Administración (usuarios y sucursales)
    path('adminapp/sucursales/', views_admin.SucursalListView.as_view(), name='sucursal_list'),
    path('adminapp/sucursales/nueva/', views_admin.SucursalCreateView.as_view(), name='sucursal_create'),
    path('adminapp/sucursales/<int:pk>/editar/', views_admin.SucursalUpdateView.as_view(), name='sucursal_update'),
    path('adminapp/sucursales/<int:pk>/eliminar/', views_admin.SucursalDeleteView.as_view(), name='sucursal_delete'),

    path('adminapp/usuarios/', views_admin.UsuarioListView.as_view(), name='usuario_list'),
    path('adminapp/usuarios/nuevo/', views_admin.UsuarioCreateView.as_view(), name='usuario_create'),
    path('adminapp/usuarios/<int:pk>/editar/', views_admin.UsuarioUpdateView.as_view(), name='usuario_update'),
    path('adminapp/usuarios/<int:pk>/eliminar/', views_admin.UsuarioDeleteView.as_view(), name='usuario_delete'),

    path('reportes/', views_reportes.reportes_home, name='reportes_home'),
    path('reportes/ventas.csv', views_reportes.reporte_ventas_csv, name='reporte_ventas_csv'),
    path('reportes/ventas.xlsx', views_reportes.reporte_ventas_excel, name='reporte_ventas_excel'),
    path('reportes/dashboard/', views_reportes.reportes_dashboard, name='reportes_dashboard'),


]
