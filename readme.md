Versión Python: `3.6`

Versión Django: `3.2.14`

## Base de Datos

La app usa base de datos postgres proporcionada por heroku para tener los datos en la web.

## Instale requerimientos

pip3 install -r requeriments.txt

pip install -r requeriments.txt

## Correr server

python3 manage.py runserver

python manage.py runserver

## Superuser

Username: USEIT
email: nicolashurtado0712@gmail.com
password: prueba123

## Documentación

Se implementa Swagger la cual especifica la lista de recursos disponibles en la API REST y las operaciones a las que se puede llamar en estos recursos,
permite probar los servicios de forma extremadamente sencilla  -> http://127.0.0.1:8000/api/schema/swagger-ui/

## Correr con docker 

docker build -t useit .

docker run --name useit_app -p 8000:8000 -d useit

