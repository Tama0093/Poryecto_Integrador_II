from django.contrib import admin
from .models import Sucursal, Perfil
from .models import Producto
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'sucursal', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('sucursal', 'fecha_creacion')

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono', 'created_at')
    search_fields = ('nombre', 'direccion')

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'sucursal')
    search_fields = ('user__username', 'sucursal__nombre')

# Mostrar perfil en el admin del User (inline)
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

# Re-registrar User admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
