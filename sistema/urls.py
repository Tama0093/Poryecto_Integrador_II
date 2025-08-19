# sistema/urls.py
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path('admin/', admin.site.urls),
    # Rutas de la app (home, login/logout, productos, caja, admin-app)
    path('', include('inventario.urls')),
]
