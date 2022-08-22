from django.urls import path
from .views import *


urlpatterns = [
    path("admin/",  Administrator.as_view(), name="Administrator"),
    path("admin/<int:id>/",  DetailAdministrator.as_view(), name="DetailAdministrator"),
    path("empresa/",  Empresas.as_view(), name="Empresas"),
    path("empresa/<int:id>/",  DetalleEmpresas.as_view(), name="DetalleEmpresas"),
    path("empleado/",  Empleado.as_view(), name="Empleado"),
    path("empleado/<int:id>/",  DetalleEmpleado.as_view(), name="DetalleEmpleado"),
]