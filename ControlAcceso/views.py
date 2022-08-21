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
            print(request.user.is_superuser)
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
    
    # def delete(self, request, id):
        
    #     try:
    #         PQRTy = PQRTypes.objects.get(id=id)
    #     except PQRTypes.DoesNotExist:
    #         PQRTy = None

    #     if not PQRTy:
    #         return Response({"res": f"El objeto con el id: {id} no existe"},status=status.HTTP_400_BAD_REQUEST)

    #     PQRTy.delete()
    #     return Response({"res": f"Tipo de PQR con id: {id} ha sido eliminado!"}, status=status.HTTP_200_OK)