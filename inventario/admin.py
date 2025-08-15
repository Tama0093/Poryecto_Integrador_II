from django.contrib import admin
from .models import Sucursal, Perfil
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Caja, Venta

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono', 'created_at')
    search_fields = ('nombre', 'direccion')

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'get_sucursales')
    search_fields = ('user__username', 'sucursales__nombre')
    filter_horizontal = ('sucursales',)  # 👈 selector múltiple en la vista de Perfil

    def get_sucursales(self, obj):
        return ", ".join([s.nombre for s in obj.sucursales.all()])
    get_sucursales.short_description = 'Sucursales'

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'
    filter_horizontal = ('sucursales',)  # 👈 selector múltiple también dentro del inline

    # Evitar duplicado al crear usuario (el perfil lo crea la señal post_save)
    def get_extra(self, request, obj=None, **kwargs):
        # Si estás en "agregar usuario" (obj=None), no muestres formulario inline
        # para que no intente crear un Perfil manual y choque con la señal.
        return 0 if obj is None else (0 if hasattr(obj, 'perfil') else 1)

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)


@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ('sucursal', 'fecha', 'apertura_monto', 'cierre_monto', 'estado', 'creado_en')
    list_filter = ('sucursal', 'estado', 'fecha')
    search_fields = ('sucursal__nombre',)

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('caja', 'producto', 'cantidad', 'precio_unitario', 'total', 'usuario', 'creado_en')
    list_filter = ('caja__sucursal', 'producto', 'usuario', 'creado_en')
    search_fields = ('producto__nombre', 'usuario__username')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
