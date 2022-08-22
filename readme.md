Versión Python: `3.6`

Versión Django: `3.2.14`

## Funcion de la Aplicación

-  El usuario administrador(superusuario) de la aplicación puede crear empresas.

-  El usuario administrador(superusuario) de la aplicación puede crear un usuario
administrador para cada empresa creada e invitarlo por correo electrónico.

-  El usuario administrador de cada empresa debe poder gestionar puntos de acceso de la
empresa (sedes).

-  El usuario administrador de la empresa puede invitar a un empleado de la organización a registrarse con un vínculo dentro de un correo electrónico, el usuario se registra como perteneciente a la empresa.Este vínculo debe llevar a un formulario de registro donde el usuario llenará sus datos básicos.

- El usuario administrador de la organización puede asignar a un usuario empleado de su
empresa a un punto de acceso (sede ) y debe poder especificar varias franjas horarias
dentro de la cual dicho empleado podrá acceder a la sede.

-  El administrador debe poder activar o desactivar accesos a cada sede.

## Base de Datos

La app usa base de datos postgres proporcionada por heroku para tener los datos en la web.

## Instale requerimientos

pip3 install -r requeriments.txt

pip install -r requeriments.txt

## Correr server

python3 manage.py runserver

python manage.py runserver


## Documentación

Se implementa Swagger la cual especifica la lista de recursos disponibles en la API REST y las operaciones a las que se puede llamar en estos recursos,
permite probar los servicios de forma extremadamente sencilla  -> http://127.0.0.1:8000/api/schema/swagger-ui/

## Correr con docker 

docker build -t useit .

docker run --name useit_app -p 8000:8000 -d useit

