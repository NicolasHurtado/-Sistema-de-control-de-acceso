"""Useit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from ControlAcceso.views import  LoginView, LogoutView, ConfirmarEmail, Registro, CorreoRegistro, IngresoEmpleado


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',LoginView.as_view(), name='auth_login'),
    path('logout/',LogoutView.as_view(), name='auth_logout'),
    path('confirmar/',ConfirmarEmail.as_view(), name='ConfirmarEmail'),
    path('registro/', Registro, name='Registro'),
    path('correo_registro/', CorreoRegistro.as_view(), name='CorreoRegistro'),
    path('ingreso_empleado/', IngresoEmpleado.as_view(), name='IngresoEmpleado'),
    path('control/', include('ControlAcceso.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
]
