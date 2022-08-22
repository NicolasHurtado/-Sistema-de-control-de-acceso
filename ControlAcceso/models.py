from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django import forms

# Create your models here.
class User(AbstractUser):
    estado = models.BooleanField(default=False)
    class Meta:
        db_table = 'auth_user'


class Empresa(models.Model):
    admin_user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name=" Usuario administrador")
    nit = models.CharField(max_length=50, verbose_name="Nit", unique=True)
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la empresa")
    nombre_comercial = models.CharField(max_length=200, verbose_name="Nombre comercial de la empresa")
    direccion = models.CharField(max_length=200, verbose_name="Direccion")
    telefono = PhoneNumberField(verbose_name="Numero de celular")
    email = models.EmailField(max_length=200, verbose_name="Correo electrónico")
    sitio_web = models.CharField(max_length=200, verbose_name="Sitio web")
    ubicacion = models.CharField(max_length=350, verbose_name="País, Estado y Ciudad")

    class Meta:
        db_table = "empresas"
    
    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    identificacion =  models.CharField(max_length=50, verbose_name="Numero de Identificación", unique=True)
    nombre = models.CharField(max_length=50, verbose_name="Nit")
    apellido = models.CharField(max_length=200, verbose_name="Nombre de la empresa")
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE, verbose_name="Empresa")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    telefono = PhoneNumberField(verbose_name="Numero de celular")
    email = models.EmailField(max_length=200, verbose_name="Correo electrónico")
    ubicacion = models.CharField(max_length=350, verbose_name="País, Estado y Ciudad")
    
    
    class Meta:
        db_table = "usuarios"
    
    def __str__(self):
        return self.nombre

class Sucursal(models.Model):
    Estados = [
        ('activo', 'activo'),
        ('inactivo', 'inactivo')
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    email = models.EmailField(max_length=200, verbose_name="Correo electrónico")
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE, verbose_name="Empresa")
    telefono = PhoneNumberField(verbose_name="Numero de celular")
    geolocalizacion = models.CharField(max_length=350, verbose_name="Geolocalización")
    estado = models.CharField(max_length=8, choices=Estados, default='activo',verbose_name="Estado del punto")

    class Meta:
        db_table = "sucursales"
    
    def __str__(self):
        return self.nombre

class Horario(models.Model):
    hora_inicial = models.TimeField()
    hora_finalizacion = models.TimeField()
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE, verbose_name="Usuario")

    class Meta:
        db_table = "horarios"
    
    def __str__(self):
        return str(self.usuario.id)

class Asignacion(models.Model):
    horario = models.ForeignKey(Horario,on_delete=models.CASCADE, verbose_name="Horario de Usuario")
    sucursal = models.ForeignKey(Sucursal,on_delete=models.CASCADE, verbose_name="Sucursal de Empresa")

    class Meta:
        db_table = "asignaciones"
    
    def __str__(self):
        return self.pk
