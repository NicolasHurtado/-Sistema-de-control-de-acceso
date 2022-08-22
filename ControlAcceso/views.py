from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.conf import settings
from django.core.mail import send_mail
from .models import *
from .serializers import *
from .utils.utils import *

# Create your views here.

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class LoginView(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        if not request.user.is_authenticated:
            # Recuperamos las credenciales y autenticamos al usuario
            username = request.data.get('username', None)
            password = request.data.get('password', None)
            user = authenticate(username=username, password=password)

            # Si es correcto añadimos a la request la información de sesión
            if user:
                if not user.estado:
                    return Response({'res': 'El usuario no ha activado la cuenta'},status=status.HTTP_401_UNAUTHORIZED)
                login(request, user)
                return Response({'res': 'Sesión iniciada'},status=status.HTTP_200_OK)
            else:
                # Si no es correcto devolvemos un error en la petición
                return Response({'res': 'Usuario y/o contraseña invalido'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'res': 'Ya hay una sesion activa'},status=status.HTTP_401_UNAUTHORIZED)



class LogoutView(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        # Borramos de la request la información de sesión
        if request.user.is_authenticated:
            logout(request)
            # Devolvemos la respuesta al cliente
            return Response({'res': 'Sesión terminada'},status=status.HTTP_200_OK)
        else:
            # Devolvemos la respuesta al cliente
            return Response({'res': 'No hay una sesion activa'},status=status.HTTP_400_BAD_REQUEST)
    
class ConfirmarEmail(GenericAPIView):
    def get(self, request):
        token = request.query_params.get("token")
        if not token:
            return Response({'res': 'No ha enviado token'},status=status.HTTP_400_BAD_REQUEST)
        
        data_token = decode_token(token)
        if not data_token:
            return Response({'res': 'Token invalido'},status=status.HTTP_400_BAD_REQUEST)
        
        print(data_token)
        user= User.objects.get(username=data_token["username"])
        user.estado = True
        user.save()
        
        return Response({'res': 'Cuenta Confirmada'},status=status.HTTP_200_OK) 

class Administrator(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self,request):
        if request.user.is_superuser:
            print(request.user.is_staff)
            print(request.user.username)
            print(request.user.email)
            print(request.user.user_permissions.all())
            #print(request.user.has_perm("ControlAcceso.delete_user"))
            Admin = User.objects.all()
            serializer = AdministratorSerializer(Admin, many=True)
                
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({"res": "No tienes permiso para esta accion"},status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request):
        if request.user.is_superuser:
            serializer = AdministratorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                token = create_token({'email': request.data["email"], 'username': request.data["username"]})
                url = f"http://127.0.0.1:8000/confirmar/?token={token}"
                msj = f"""Para activar la cuenta ingrese a este link {url}"""
                sbj = f"""ACTIVACIÓN DE CUENTA"""
                send_mail(
                        subject=sbj,
                        message=msj,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[request.data["email"]],
                        
                    )
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"res": "No tienes permiso para esta accion"},status=status.HTTP_403_FORBIDDEN)

class DetailAdministrator(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self,request, id):
        if request.user.is_superuser:
            try:
                Admin = User.objects.get(id=id)
            except User.DoesNotExist:
                Admin = None
            if Admin:
                serializer = AdministratorSerializer(Admin,many=False)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({"res": f"El objeto con el id: {id} no existe"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"res": "No tienes permiso para esta accion"},status=status.HTTP_403_FORBIDDEN)
            
        
    
    def put(self, request, id):
        if request.user.is_superuser:
            try:
                Admin = User.objects.get(id=id)
            except User.DoesNotExist:
                Admin = None
            
            if not Admin:
                return Response({"res": f"El objeto con el id: {id} no existe"},status=status.HTTP_400_BAD_REQUEST)

            serializer = AdministratorSerializer(instance = Admin, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"res": "No tienes permiso para esta accion"},status=status.HTTP_403_FORBIDDEN)
    

    def delete(self, request, id):
        if request.user.is_superuser:
            try:
                Admin = User.objects.get(id=id)
            except User.DoesNotExist:
                Admin = None

            if not Admin:
                return Response({"res": f"El Usuario con el id: {id} no existe"},status=status.HTTP_400_BAD_REQUEST)
            
            Admin.delete()
            
            return Response({"res": f"Usuario {Admin.username} ha sido eliminado!"}, status=status.HTTP_200_OK)
        else:
            return Response({"res": "No tienes permiso para esta accion"},status=status.HTTP_403_FORBIDDEN)

class Empresas(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self,request):
        if request.user.is_superuser:
            Emp = Empresa.objects.all()
            serializer = EmpresaSerializer(Emp, many=True)
                
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({"res": "No tienes permiso para esta accion"},status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request):
        if request.user.is_superuser:
            serializer = EmpresaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                msj = f"""Bienvenido a la {request.data["nombre"]} como Administrador """
                sbj = f""" ADMINISTRADOR {request.data["nombre"]} """
                admin = User.objects.get(id=request.data["admin_user"])
                send_mail(
                        subject=sbj,
                        message=msj,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[admin.email],
                    )
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"res": "No tienes permiso para esta accion"},status=status.HTTP_403_FORBIDDEN)

class DetalleEmpresas(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self,request, id):
        if request.user.is_superuser:
            try:
                Emp = Empresa.objects.get(id=id)
            except Empresa.DoesNotExist:
                Emp = None
            if Emp:
                serializer = EmpresaSerializer(Emp,many=False)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({"res": f"La empresa con el id: {id} no existe"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"res": "No tienes permiso para esta accion"},status=status.HTTP_403_FORBIDDEN)
            
        
    
    def put(self, request, id):
        if request.user.is_superuser:
            try:
                Emp = Empresa.objects.get(id=id)
            except Empresa.DoesNotExist:
                Emp = None
            
            if not Emp:
                return Response({"res": f"La Empresa con el id: {id} no existe"},status=status.HTTP_400_BAD_REQUEST)

            serializer = EmpresaSerializer(instance = Emp, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"res": "No tienes permiso para esta accion"},status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, id):
        if request.user.is_superuser:
            try:
                Emp = Empresa.objects.get(id=id)
            except Empresa.DoesNotExist:
                Emp = None

            if not Emp:
                return Response({"res": f"La Empresa con el id: {id} no existe"},status=status.HTTP_400_BAD_REQUEST)

            Emp.delete()
            return Response({"res": f"Empresa {Emp.nombre} ha sido eliminada!"}, status=status.HTTP_200_OK)
        else:
            return Response({"res": "No tienes permiso para esta accion"},status=status.HTTP_403_FORBIDDEN)


#Clase para envio de correo de registro de empleado
class CorreoRegistro(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self,request):
        if request.user.is_staff:
            admin = request.user.id
            print(admin)
            try:
                emp = Empresa.objects.get(admin_user=admin)
            except Empresa.DoesNotExist:
                emp = None
            print(emp)

            if emp:
                token = create_token({'email': request.data["correo_destinatario"],'id_empresa': emp.id, 'nombre_empresa': emp.nombre })
                url = f"http://127.0.0.1:8000/registro/?token={token}"
                msj = f"""Para registrar sus datos ingrese a este link {url}"""
                sbj = f"""FORMULARIO DE REGISTRO {emp.nombre.upper()}"""

                send_mail(
                        subject=sbj,
                        message=msj,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[request.data["correo_destinatario"]],
                )
                return Response({"res": "Correo enviado correctamente"},status=status.HTTP_200_OK)

            return Response({"res": "No estás asignado una empresa"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"res": "No tienes permiso para esta accion"},status=status.HTTP_403_FORBIDDEN)


# Plantilla de formulario de registro de empleado
@api_view(['GET','POST'])
@renderer_classes([JSONRenderer,TemplateHTMLRenderer])
def Registro(request):
    token = request.query_params.get("token")
    print(token)
    if not token:
        return JsonResponse({'res': 'No ha enviado token'},status=status.HTTP_400_BAD_REQUEST)
    
    data_token = decode_token(token)
    if not data_token:
        return JsonResponse({'res': 'Token invalido'},status=status.HTTP_400_BAD_REQUEST)
    
    print(data_token)
    nombre_empresa = data_token["nombre_empresa"]
    id_empresa = data_token["id_empresa"]
    email = data_token["email"]
    print(nombre_empresa)
    print(id_empresa)
    print(email)
    context = {
        'nombre_empresa': nombre_empresa,
        'id_empresa': id_empresa,
        'email': email
    }
    return render(request,'registro.html', context, status=status.HTTP_200_OK)

# Empleados
class Empleado(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self,request):
        if request.user.is_superuser:
            print(f"Soy superusuario {request.user}")
            print(request.user.has_perm("ControlAcceso.add_usuario"))
            Empleados = Usuario.objects.all()
            serializer = EmpleadoSerializer(Empleados, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif request.user.is_staff:
            admin = request.user.id
            print(f"Soy Administrador {request.user}")
            print(request.user.has_perm("ControlAcceso.add_usuario"))
            try:
                Emp = Empresa.objects.get(admin_user=admin)
            except Empresa.DoesNotExist:
                Emp = None
            
            if Emp:
                Empleados = Usuario.objects.filter(empresa=Emp)
                
                if Empleados:  
                    serializer = EmpleadoSerializer(Empleados, many=True)  
                    return Response(serializer.data,status=status.HTTP_200_OK)
                
                return Response({"res": f"No tienes empleados en tu empresa ({Emp.nombre})"},status=status.HTTP_400_BAD_REQUEST)

            return Response({"res": "No estas asignado una empresa"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"res": "No tienes permiso para esta accion"},status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request):
        token = request.META.get('CSRF_COOKIE', None)
        print(token)
        if not token:
            return Response({'res': 'No ha enviado token'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = EmpleadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DetalleEmpleado(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self,request, id):
        if request.user.is_staff:
            admin = request.user.id
            try:
                empresa = Empresa.objects.get(admin_user=admin)
            except Empresa.DoesNotExist:
                empresa = None
            
            if empresa:
                try:
                    Empleado = Usuario.objects.get(id=id,empresa=empresa)
                except Usuario.DoesNotExist:
                    Empleado = None
            else:
                return Response({"res": "No estas asignado una empresa"},status=status.HTTP_403_FORBIDDEN)
            
            if Empleado:
                serializer = EmpleadoSerializer(Empleado,many=False)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({"res": f"Usuario invalido"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"res": "No tienes permiso para esta accion"},status=status.HTTP_403_FORBIDDEN)
            
        
    
    def put(self, request, id):
        if request.user.is_staff:
            try:
                Emp = Empresa.objects.get(id=id)
            except Empresa.DoesNotExist:
                Emp = None
            
            if not Emp:
                return Response({"res": f"El objeto con el id: {id} no existe"},status=status.HTTP_400_BAD_REQUEST)

            serializer = EmpleadoSerializer(instance = Emp, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"res": "No tienes permiso para esta accion"},status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, id):
        if request.user.is_staff:
            try:
                Emp = Empresa.objects.get(id=id)
            except Empresa.DoesNotExist:
                Emp = None

            if not Emp:
                return Response({"res": f"La Empresa con el id: {id} no existe"},status=status.HTTP_400_BAD_REQUEST)

            Emp.delete()
            return Response({"res": f"Empresa {Emp.nombre} ha sido eliminada!"}, status=status.HTTP_200_OK)
        else:
            return Response({"res": "No tienes permiso para esta accion"},status=status.HTTP_403_FORBIDDEN)