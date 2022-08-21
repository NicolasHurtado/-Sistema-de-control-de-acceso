from django.urls import path
from .views import *


urlpatterns = [
    path("admin/",  Administrator.as_view(), name="Administrator"),
    path("admin/<int:id>/",  DetailAdministrator.as_view(), name="DetailAdministrator")
]