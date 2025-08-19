# inventario/admin.py
from django.contrib import admin
from .models import Sucursal, Perfil, Caja, Venta, Producto


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono')
    search_fields = ('nombre', 'direccion', 'telefono')


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'sucursal')
    list_filter = ('rol', 'sucursal')
    search_fields = ('user__username', 'rol')


@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ('sucursal', 'fecha', 'estado', 'apertura_monto', 'cierre_monto')
    list_filter = ('estado', 'sucursal', 'fecha')
    search_fields = ('sucursal__nombre',)
    date_hierarchy = 'fecha'


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'total', 'caja', 'usuario', 'creado_en')
    list_filter = ('caja__sucursal', 'caja__fecha')
    search_fields = ('producto__nombre', 'usuario__username')
    date_hierarchy = 'creado_en'


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sucursal', 'precio', 'stock', 'fecha_creacion')
    list_filter = ('sucursal',)
    search_fields = ('nombre', 'descripcion')
