# inventario/apps.py
from django.apps import AppConfig

class InventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventario'

    def ready(self):
        # Carga señales si existen (creación automática de Perfil)
        import inventario.signals  # noqa: F401
