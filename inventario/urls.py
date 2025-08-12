from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from inventario import views  # ✅ Importar vistas desde la app inventario

urlpatterns = [
    # Página de inicio
    path('', views.home, name='home'),

    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
