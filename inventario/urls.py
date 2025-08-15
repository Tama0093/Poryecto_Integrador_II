from django.urls import path
from . import views
from . import views_productos
from . import views_caja   # 👈 importante

urlpatterns = [
    path('', views.home, name='home'),

    # Productos
    path('productos/', views_productos.ProductoListView.as_view(), name='producto_list'),
    path('productos/nuevo/', views_productos.ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', views_productos.ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/eliminar/', views_productos.ProductoDeleteView.as_view(), name='producto_delete'),

    # Caja & Ventas
    path('caja/', views_caja.caja_estado_hoy, name='caja_estado_hoy'),
    path('caja/abrir/', views_caja.caja_abrir, name='caja_abrir'),
    path('caja/<int:caja_id>/', views_caja.caja_detalle, name='caja_detalle'),
    path('caja/<int:caja_id>/venta/', views_caja.venta_nueva, name='venta_nueva'),
    path('caja/<int:caja_id>/cerrar/', views_caja.caja_cerrar, name='caja_cerrar'),
]
