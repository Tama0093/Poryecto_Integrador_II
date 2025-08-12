from django.contrib import admin
from .models import Sucursal, Perfil
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono', 'created_at')
    search_fields = ('nombre', 'direccion')

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'get_sucursales')
    search_fields = ('user__username', 'sucursales__nombre')

    def get_sucursales(self, obj):
        return ", ".join([s.nombre for s in obj.sucursales.all()])
    get_sucursales.short_description = 'Sucursales'

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'

    # Evitar duplicado
    def get_extra(self, request, obj=None, **kwargs):
        return 1 if obj and not hasattr(obj, 'perfil') else 0

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
