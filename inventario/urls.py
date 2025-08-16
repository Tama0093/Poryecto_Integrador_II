from django.urls import path
from . import views
from .views_productos import (
    ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView
)
from . import views_caja   
from . import views_admin 

urlpatterns = [
    path('', views.home, name='home'),

    # Productos
    path('productos/', ProductoListView.as_view(), name='producto_list'),
    path('productos/nuevo/', ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/eliminar/', ProductoDeleteView.as_view(), name='producto_delete'),

    # Caja & Ventas
    path('caja/', views_caja.caja_estado_hoy, name='caja_estado_hoy'),
    path('caja/abrir/', views_caja.caja_abrir, name='caja_abrir'),
    path('caja/<int:caja_id>/', views_caja.caja_detalle, name='caja_detalle'),
    path('caja/<int:caja_id>/venta/', views_caja.venta_nueva, name='venta_nueva'),
    path('caja/<int:caja_id>/cerrar/', views_caja.caja_cerrar, name='caja_cerrar'),

    # Admin web
    path('adminweb/usuarios/crear/', views_admin.crear_usuario, name='crear_usuario'),
    path('adminweb/sucursales/crear/', views_admin.crear_sucursal, name='crear_sucursal'),

    path('crear-usuario/', views_admin.crear_usuario, name='crear_usuario'),
    path('crear-sucursal/', views_admin.crear_sucursal, name='crear_sucursal'),
]
